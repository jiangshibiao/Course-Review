## Array
+ 导入：`import java.util.List;`
+ 重载
    1. 在排序的类里重载：定义类后面加上 `public class App implements Comparable<App>`。
	~~~Java
        public int compareTo(App app) {
            return ;
        }
    ~~~
    2. 新开一个类重载
    ~~~Java
        class MyComparator implements Comparator<Integer>{
            @Override
            public int compare(Integer o1, Integer o2) {
                return o2-o1;
            }
        }
    ~~~

## 容器的普遍接口 Collection

<img src="Collection.png" style="zoom:50%;" />

+ 只能放对象，不能放 `primitive data`
+ 子类的 Collection 不能看做是继承了父类的 Collection（不能赋值）
	- `Collection <?>`
	- `Collection <? extends father>`
	- `static <T> void fromArraytoCollection(T[]a, Collection<T>c)`
+ 用 `for each` 进行遍历
+ 用 `Iterator` 访问
	- iterator()
	- next()
	- hasNext()
+ 函数和方法
    - add()
    - addAll(Collecton)
    - containsKey()
    - remove()
    - isEmpty()
    - size()
    - clear()
    - toArray()
+ Collections 的静态方法 
    - max(Collection) , min(Collection) 
    - reverse( ) 
    - copy(List dest, List src)
    - fill(List list, Object o)

## Generic 泛型

+ A generic type declaration is compiled once and for all, and turned into a single class file.
+ In general, if `Foo` is a subtype (subclass or subinterface) of `Bar`, and `G` is some generic type declaration, it is not the case that `G` is a subtype of `G`.
+ 泛型可以在编译期进行类型检查，并且仅在编译期有效。**所有泛型参数类型在编译后都会被清除**。
    + A Generic Class is Shared by all its Invocations.
      ```java
        List <String> l1 = new ArrayList<String>();
        List<Integer> l2 = new ArrayList<Integer>();
        System.out.println(l1.getClass() == l2.getClass()); //true
      ```
    + **不能对确切的泛型类型使用 instanceof 操作**。
         ```java
          if (cs instanceof Collection<String>) { ...} // illegal
          //Error: Cannot perform instanceof check against parameterized type Collection<String>. Use the form Collection<?> instead since further generic type information will be erased at runtime
         ```
    + 泛型数组初始化时不能声明泛型类型。 如下代码编译时通不过：
        ```java
        List<String>[] list = new List<String>[];
        ```
        - 在这里可以声明一个带有泛型参数的数组，但是不能初始化该数组，因为执行了类型擦除操作后，List<Object>[] 与 List<String>[] 就是同一回事了，编译器拒绝如此声明。
    
+ Wildcards vs. Generic
    + Wildcards are designed to support flexible subtyping. 
    + Generic methods allow type parameters to be used to express dependencies among the types of one or more arguments to a method and/or its return type.
    + ```JAVA
      public static <T> void copy (List<T> dest, List<? extends T> src){...} 
      ```
## Iterator
+ An iterator is an object whose job is to move through a sequence of objects and select each object in that sequence without the client programmer knowing or caring about the underlying structure of that sequence.
  + iterator(): Return the first element
  + next(), hasNext()
  + remove(): Removes from the underlying collection the last element returned by this iterator.

## List
+ 分类
	- ArrayList
	  - It keeps its own private count of how many items it is currently storing. 
	  - Its size method returns the number of objects currently stored in it. 
	- LinkedList
	- List $\rightarrow$ Vector $\rightarrow$ Stack
	- Queue

## Set

+ 分类
	- HashSet
	- TreeSet
+ 重载：复写类中的 hashCode() 函数和 equals() 函数。


## Map

+ 导入：`import java.util.List;`
+ 定义： `HashMap<String, String> map = new HashMap<>();`
+ 迭代
	~~~Java
        for (Entry<String, String> entry : map.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
        }
  ~~~
