# 背景
为了满足对代码功能模块的定制，新增feature模块，其可以方便模块化功能的去与留，涉及makefile，c/c++，java等三个部分。开发者只需要定义一个值，在编译时会自动生成三个代码空间的控制变量，以此达到定义功能模块的目的。
feature分为两个层级：

- common
- 具体产品名，比如lemonadep

一个feature开关可以同时在common和具体产品名中定义，他们的关系是：

- 当只有common中有定义时，以common为准
- 当只有具体产品中有定义时，以产品名为准
- 当同时定义时，产品名中的定义会overlay common中的定义

# 结构说明
```bash
feature
├── Android.bp
├── build_out
│   ├── include
│   │   └── JosFeature.h
│   ├── java
│   │   └── com
│   │       └── journeyOS
│   │           └── JosFeature.java
│   └── makefile
│       └── JosFeature.mk
├── jos_feature.mk
├── common_feature.mk
├── device
│   ├── common
│   │   └── features.cof
│   └── lemonadep
│       └── features.cof
└── tools
    ├── config_parse.py
    ├── feature.py
    ├── generator_header.py
    ├── generator_java.py
    ├── generator_makefile.py
    ├── __init__.py
    └── utils.py
```
其中目录大致说明如下：

- tools：编译工具，用于生成对应目标代码文件
- device/common：通用控制定义文件
- device/lemonadep：产品控制定义文件
- jos_feature.mk：feature引入编译系统makefile
- common_feature.mk：定义一些aosp的宏，如 **TARGET_EXCLUDES_AUDIOFX := true** , 则表示不编译audiofx到rom中。
# 使用方法
feature使用方法很简单，分成两个部分：

- feature定义
- 代码使用
## feature定义
一般来说，feature的定义如下所示：
```java
device/common/features.cof

# jos feature default
JOS_FEATURE_DEFAULT = 1
# jos ai service
JOS_FEATURE_AI_SERVICE = false
#jos device
JOS_FEATURE_DEVICE = "lemonadep"
```
这类似于.ini文件，是键值对的定义。下面说明基本语法。
### 注释
feature定义只支持单行注释，注释是以"**#**"开头。
```java
# jos feature default
JOS_FEATURE_DEFAULT = 1
```
### 键值对
键值对定义格式为：**KEY = VALUE**。如下：
```java
JOS_FEATURE_AI_SERVICE = false
```
其中key的命名规范为：A-Z，a-z，0-9，_，这些字符的组成，开头首字母不能是数字。
value支持的类型

| **类型** | **解析器定义** | **说明** | **举例** |
| --- | --- | --- | --- |
| int | TYPE_INT | 整数类型 | JOS_FEATURE_DEFAULT = 1 |
| boolean | TYPE_BOOLEAN | 布尔类型 | JOS_FEATURE_AI_SERVICE = false |
| String | TYPE_STRING | 字符类型 | JOS_FEATURE_DEVICE = "lemonadep" |

## 代码使用
feature可以在三个代码空间使用：

- java
- c/cpp
- makefile

编译完成后，上述的代码会生成到：feature/build_out/ 目录下。
### java
java中使用feature时，先import com.journeyOS.JosFeature，然后就可以直接使用对应的变量了。如下：
```java
import com.journeyOS.JosFeature

if (JosFeature.JOS_FEATURE_AI_SERVICE) {
    //TODO
}
```
### c/c++
C中定义的都是宏变量，使用方法举例如下：
```java
#include <product/JosFeature.h>

#if JOS_FEATURE_AI_SERVICE

//TODO

#endif

```
### Makefile
mk中可以直接使用，比如：
```java

ifeq ($(JOS_FEATURE_AI_SERVICE),true)

# TODO

endif
```

# 代码原理
features.cof是由python脚本来解释的，解释程序的路径为：feature/tools/。整个feature实现比较简单，处理流程分如下几个步骤：

- 将jos_feature.mk文件添加到android的编译系统中（build/core/product_config.mk）。
- 当lunch的时候，会先运行feature.py解析feature.def文件
- config_parse.py先会检查feature.def文件的语法错误
- 错误检查通过后，config_parse.py继续将feature.def文件转换成字典
- 将生成的字典分别提交给不同code的生成者生成对应的代码。

# 总结
综上，feature功能是一个在编译期用python脚本解析features.cof文件，生成三个代码空间的控制变量代码文件，最终被静态添加到目标程序中的过程。

# 附加
生成的com.journeyOS.JosFeature还可以编译到framework.jar中

