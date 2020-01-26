## Paper summary

#### Brief introduction: The Seletor Model

+ Selectors are an **extension** of the Actor model
	- like actors, a selector is an execution unit that has the capability to process incoming messages
+ Motivation: Backwards of Actors
	- doesn't permit shared state
	- All communication is **asynchronous**, difficult for concurrent coordination involving multiple actors
+ Features
	- **multiple mailboxes** to receive messages
		+ help to cope with messages of different priority or purpose
		+ can be executed concurrently or asynchronously by adding to different mailboxes
	![](SelectModel.png)
	- Each mailbox has a **boolean condition** (which is called **guard**)
		+ It's used to enable or disable a specific mailbox while processing a message
		+ Guard does not affect the mailbox’s ability to receive messages
	- More operations about multiple mailboxes
		- The message sender can directly **specify the mailbox** to send a message to
		- If the messages come without targent mailbox, the receiver can **determine where** to put them, or even trigger some guards.
		- Besides modified by the selector, guards can **be declared with explicit expressions** (just like expressions in digital logic circuits)
+ Life Cycle
	- **new**
		+ not guaranteed to instantiate immediately after creation
		+ An access handle is immediately created and passed to the caller and any entity holding this handle can start sending messages to the selector.
	- **started**
		+ processes messages one at a time from any enabled mailbox
		+ can enable or disable guards
		+ process messages in mailboxes of higher priority first
		+ rotates between mailboxes with same priority
	- **terminated**
		+ terminate when `exit()` is called
		+ not process any messages in its mailbox and ignores all incoming messages
		+  The distributed runtime **does not terminate this selector** immediately **until** all new operations requested by this selector are observed to have completed and no outgoing messages remain in the local buffer.

#### Some Example Patterns

+ Synchronous Request-Reply Pattern
	- Task
		+ The replier receives messages from the requestor and respones to it after processing messages.
		+ The requestor **doesn't do anything** until receiving responsing messages.
	- Designs for Actor Models
		+ The sender stalls all other computations until it receives the corresponding reply
		+ The incoming messages before the response message must be stashed and unstashed to the mailbox after processing the reply message
		+ hard to implement efficiently
	- Solutions for Selectors
		+  Define **two separate mailboxes**, one to receive **regular messages** including all the request messages and another mailbox to receive **only synchronous response messages**.
		+ When a receiver expected to process a synchronous response message, disables the REGULAR mailbox (ensures that the next message to be processed will be from the REPLY mailbox) until finish it.

+ Join Patterns in Streaming Applications
	- Task
		+ Messages from two or more data streams are combined into a single message.
		+ Receivers need to match the data from all sources and wait for all the data to arrive before processing the messages.
		![](JoinPattern.png)
	- Designs for Actor Models
		+ **The order of processing of messages is not guaranteed** on the sender actors
		+ Keep a track of all the in-flight messages from various sequence numbers.
		+ Only when messages from all the source actors for the oldest sequence number is received by the aggregator actor, it can reduce the items into a single value.
	- Solutions 1 for Selectors: **Any order**
		+ The number of mailboxes the receiver has is just the number of sources.
		+ All mailboxes are enabled at first. When receiving a message from source $i$, disable mailbox $i$.
		+ If matchsized size reaches the specific number, process these messages and  enable all messages.
	- Solutions 2 for Selectors: **Robin order**
		+ Only mailbox $0$ is enabled at first. When receiving a message from source $i$, disable mailbox $i$ and enable mailbox $i+1$.
		+ If $matchsize$ reaches the specific number, process these messages. Then enable mailbox $0$ and repeat.

+ Producer-Consumer with Bounded Buffer
	- Task
		+ the producer pushes work into the buffer as work is produced and the consumer pulls work from the buffer when they are ready to execute.
	- Designs for Actor Models
		+ Build three actors played each of role.
		+ **Lots of details should be considered**.
		+ a) When the buffer is empty, and the consumer requests work, then the consumer is placed in a queue until work is available.
		+ b) When producers are ready to produce data, and the buffer is full, the producer is placed in a queue until the buffer is empty.
		+ Additional complexity is observed as the buffer actor also needs to maintain queues for the available producers and consumers.
	- Solutions for Selectors
		+ The buffer handles two mailboxes, one for producer and other for consumer.
		+ Simply use the following **explicit expressions**:
		`guard(MBX_PRODUCER , dataBuffer .size () < thresholdSize )`
		`guard(MBX_CONSUMER ,!dataBuffer .isEmpty ())`

## Design Workflow

+ System Structure
	![](DSSystem.png)
    - The structure in one unit (which is called **place** or **node**)
    	+ One **System Actor**: maintains the internal state, as well as communicating information with other places.
    	+ One **Proxy Actor**: coordinating the messages between local and remote selectors
    	+ A **local registy**: maintained by proxy actor, stores the address of selectors located in the same place.
    	+ A series of Selectors
    - The distributed selector system
    	+ DS contains a collection of computering nodes (places).
    	+ The user can choose to denote a specific place in the configuration file as the **Master Node**, which controls system bootstrap and the global termination.

+ Initialization and Bootstrap
	- Each program is considered as a single DS. Many simple DS cound combine a large system
	- Each node is set up with configuration file and SSH access for the initial master node.
	- **Configuration files can be modified -> dynamic addition of places**
	- The System Actor on Master Node logs into each remote location through SSH, and starts up an idle HJ selector system there
	-  The system actors on each place will identify the Master Node from configuration.
	- When initialized successfully, these system actors send state to the master. The Master Node collects ready messages for all known remote places and informs each place’s proxy actor to start program execution.
	- Optionally, users can choose to manually start up each place when each place if it is correctly setup. **This choice does not affect the automated global termination of the system**.
	![](start.png)


+ Communication among Selectors
    - Any Selector is uniquely identified by 32-bit integer
    	+ an 8-bit value encoding the place p on which the selector is created
    	+ an 8-bit value encoding the place q on which the selector instance resides
    	+ a 16-bit integer value representing a unique identifier for the selector on p
    - Use Kryo serialization framework
		+ A compromise way, which is faster than JAVA serializer and has less strictions than Google's Protocol Buffers.
		+ In theory, a selector can send and receive any message that implements `java.serializable`
	- When message is passing...
		+ If the destination place matches the local place then the Proxy Actor looks up its local registry to find the selector and forwards the message.
		+ If local registry doesn’t have an entry yet, then the Proxy Actor buffers any message to the non-existing selector. (? not explict enough ?)
		+ If the destination place is remote then the Proxy Actor forwards the message to that specified place. The Proxy Actor at the destination place will further use the local registry to forward the message to the specific selector. 
	- The implementation of building new selectors
		+ If a new selector is asked to be created **at the local place**, use **java reflections** to create without Proxy Actor.
		+ If not, the Proxy Actor sends over this message, and same thing will be done in the destination place. **The topology of the selector system is tightly coupled.**
		![](ProxyActor.png)

+ Global Termination

	- stage 1:
		+ A System Actor detects its place to be **idle** if its local user-defined selectors have all been terminated by the user, and no pending selector creation.
		+ The System Actor sends this message to Master Node, but **idle state will be reset** by any new incoming request.
		+ Master Node attempts to initiate the termination process(moves to Stage 2) if it collects idle state from all places (although some places may be re-active).
	- stage 2:
		+ The System Actor at the Master Node passes a signal to prepare termination. The path of signal passing forms a **ring** with a certain order. Every place confirms its idle state by signal down the ring, or short-circuit the ring and declare its active state, then the termination process halts.
		+ If signal competes the round trip, move to stage 3.
	- stage 3:
		+ the Master Node sends a real termination signal down the place-ring.

#### MICRO-BENCHMARKS

+ Introduction
	- The selected benchmarks uses the master-worker parallelism to achieve both **intra-node and inter-node parallelism**.
	- All implementations feature multiple mailboxes to differentiate control messages, and actual computational tasks, with control messages of higher priority.

+ Trapezoidal Approximation
	- approximates $f(x)=\frac{1}{x+1}\sqrt{1+e^{\sqrt{2x}}} \times \sin(x^3-1)$ over intervals $[a,b]$.
	- calculated in a master-worker style parallelism
	- Each worker is a selector that computes the integral approximation in parallel and send their results back to the master selector. The master selector then collects the results from all the worker selectors, adds them up, and displays the final result.
	- shows steady scalability over 2 to 12 nodes with increasing workload under minimal communication among selectors

+ Precise Pi Computation
	- a master-worker style parallelism
	- the master selector incrementally finds work and allocates fragments of the work to the worker selectors, while it collects partial results until reaching
the desired precision.

+ NQueens First K Solutions
	- Each time a worker successfully place a non-attacking queen on the partial solution, the worker reports the partial board back to master as a new work item
	- Each time a worker reports a board configuration to the Master Node selector, the master either **assigns the partial solution to a worker in a round-robin fashion** or records that a valid solution is found. (like BFS?)
	-  Exploits the priority feature in our DS implementation, places a higher priority on work items that contain complete partial solutions (i.e. **with more safely placed queens**).
	- comparison
		+ With a naive actor-based implementation, a solution limit to allow termination has no effect on the program, and the program has to exhaustively compute the solution space.
		+ Without using priority, depth-first search with a divide-and-conquer style is hard to implement, since messages are processed in their received order.
