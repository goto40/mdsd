# Language to specify structs with compile time reflection information

## Example

Models are stored in `*.item` files, e.g. `example.item`:
```
package example

    struct Point {
      scalar x : built_in.float
      scalar y : built_in.float
    }
    struct Line {
      scalar p1 : Point
      scalar p2 : Point
    }
    struct Circle {
      scalar center : Point
      scalar radius : built_in.float
    }
    struct ColoredTriangle {
      array color : built_in.float[3]
      array points : Point[3]
    }
```

You can see many examples in [framework/item_lang/tests/model/filebased_tests](https://github.com/goto40/mdsd/blob/master/framework/item_lang/tests/model/filebased_tests):
  * good*.item: good cases (valid models)
  * bad*.item: bad cases (invalid models with expected error as comment)

## Model Structure

 * The model consists of objects of the following types.
   Grammar: see our [rough architecture](architecture.md) description.
   * `Struct` (like C-structs), with data members (`Attribute`).
      Each `Attribute` can have properties (`Property`) to 
      add meta information (like `minValue`, `maxValue`,
      `defaultValue`, ...).
   * `Enum` (like C-enums)
   * `Constant` (integer or floating point constant values, either
      located in a separate `Constant` section or within a `Struct`).

 * Properties of attributes represent an optional aspect of the model.
   * Without properties, the model represents mainly structural information
     (e.g., a point with x/y attributes).
   * With properties, additional information can be included in the
     generated code (like min/max values, e.g., a point with x/y values
     which must be positive).
   * You can define additional user defined properties to your model.
     For most languages, these additional properties (maybe formatting hints
     or additional value restrictions) are included in the generate
     code (without changing the code generator itself).

### Raw Types and built in types

Raw Types identify either a floating point type or a signed/unsigned integral type of
different bit size. Normally, there is not need to define your own types, since
all usual configurations are built in (e.g. `float`, `double`, `int32`, `uint32`, ...).
You can also find special versions to be used in bitfields, like and `int5` (a 5 bit
signed integer).

### Enums

Enums are based on a integral raw type. Example:

```
package abc

    enum OnOff : built_in.bool {
        value ON = true
        value OFF = false
    }
    enum ABC : built_in.uint2 (.description="a demo enum using 2 bits") {
        value A = 0 (.description="only values from 0..3 are allowed (2 bits)")
        value B = 1 (.description="test")
        value C = 2 (.description="test")
    }
    enum SABC : built_in.int32 (.description="a demo enum using 32 bits") {
        value A = 0 (.description="test")
        value B = -1 (.description="here, negative values are allows")
        value C = 2 (.description="test")
    }
```

### Constants

Constants can be defined to be used in the model and to be exported to various target
languages. Example:

```
package abc

    constants MyConstants (.description = "example")
    {
        constant c1: built_in.uint32 = 1 (.description = "constant")
        constant c2: built_in.float = 3.4 (.description = "constant")
    }
    struct Test1 {
        constant c3: built_in.uint32 = 1 (.description = "constant")
        scalar a: built_in.uint32 (.defaultValue = 3*MyConstants.c1)
        scalar b: built_in.uint32 (.defaultValue = c3)
    }
```

### Attributes

#### Scalar Attributes

Syntax example:
```
// part of a struct:
    scalar x: built_in.float
    if (version>1) scalar extra: built_in.uint32
```

Note: scalar attributes can be embedded

#### Array Attributes

Syntax example:
```
// part of a struct:
    array a1: built_in.float[10][2]
    scalar n: built_in.uint32
    array a2: built_in.uint32[n*3]
    if (version>1) array extra: built_in.uint32[n]
```

#### Variant Attributes

Syntax example:
```
// part of a struct:
    scalar id: TypeSelector
    variant payload: id -> {
        POINT: Point
        POLY: Polygon
        TRIANGLE: Triangle
   }
```

#### Bitfields

Syntax example:
```
// part of a struct:
    scalar x: built_in.uint32
    embedded scalar r: built_in.uint2
    embedded array c: built_in.uint3[3]
    embedded scalar r: built_in.uint21
    array ok: built_in.float[r]
```

Fixed sized arrays and scalar attributes can be embedded in bitfields.
"if restrictions" may not bed used for embedded attributes or containers.

#### Restricted Attributes ("if")

You can restrict attributes to exist
only if a certain (simple) requirement
is fulfilled (e.g. a version field
is above a certain value).

With this you can - under certain 
circumstances - handle different
versions of an interface.

```
package test

struct Point {
    scalar dim: built_in.uint32 (.maxValue=3)
    scalar x: built_in.int32
    if (dim>1) scalar y: built_in.int32
    if (dim>2) scalar z: built_in.int32
}

struct Data {
    scalar version: built_in.uint32 (.maxValue=1)
    scalar n: built_in.uint32
    array data: built_in.uint32[n]
    if (version==0) array data0: built_in.uint32[n]
    if (version==1) array data1: built_in.uint32[n]
}
```

### Properties

Properties are used to enrich the model with additional meta information.
Default property definitions are built in, like `minValue` and `maxValue`.
Additional, project specific property definitions can be added to support
custom modeling aspects.

Project specific property definitions are specified in a property definition set (which can inherit from other property definition sets). You implicitely inherit from the built in property set. Thus, you cannot redefine the existing properties like `description`, `minValue`, etc.

Property definitions define where a property is applicable:
```
PropertyDefinition: 'property'
    optional?='optional'
    (('applicable' 'for'|'applicable_for') applicable_for+=ApplicableFor[','])?
    name=ID ':'
    internaltype=InternalType
    ('(' '.' 'description' '=' description=STRING ')')?
    ('{' (numberOfPropRestriction=NumberPropertiesPerStructDefRestriction)? '}')?;

NumberPropertiesPerStructDefRestriction: min=INT 'to' max=INT ('times_per_message'|'times' 'per' 'message');
// Note: "array" is used to disallow "scalars"
// Note: "scalar" is used to disallow "arrays"
ApplicableFor: ApplicableForRawType| 'struct'| 'enum' | 'array'|'scalar'|'variant'|'struct_definition';
ApplicableForRawType: 'rawtype' ('(' concrete_types+=[RawType|FQN][','] ')')?;
```
 * **optional**: means the property is optional (else it is mandatory, if applicable).
 * **applicable for**
   * if undefined, the property is applicable everywhere, except for struct definitions.
   * **array**, **scalar**, **variant**, or **struct_definition** allows arrays, scalars, variants, or struct definitions.
   * **rawtype** or **rawtype(...)** allows rawtypes or certain rawtypes.
   * **internaltype**: INT, UINT, STRING, ..., or ATTRTYPE 
     (ATTRTYPE inherits the type from the attribute to which the property is bound to;
     not applicable for struct definitions)
   * **... times per message** limits the number of properties per message
     (recursively; recursion is stopped by the flag `.is_payload=true`;
     arrays of structs or variants are not taken into account) 

Example with built in property definitions:
```
package example
    
    struct Point {
      scalar x : built_in.float (.minValue=0.1, .defaultValue=1, .maxValue=1e5)
      scalar y : built_in.float (
          .defaultValue=0x0aB,
          .description="Hello")
    }
```

Example with custom property definitions:
```
package example.one (property_set example.one.ProjExt)

    property_set ProjExt {
        property optional myprop1: STRING
        property myprop2: ATTRTYPE
    }

    struct A {
        scalar x: built_in.int32 (
            .description="a",
            .myprop1="Hello",
            .myprop2=1)
    }
```

## Model Validation

The easiest way to get an overview of validation rules is to look at the
file based tests ([framework/item_lang/tests/model/filebased_tests](https://github.com/goto40/mdsd/blob/master/framework/item_lang/tests/model/filebased_tests)). These tests illustrate the good case (with explanation)
and the bad cases (with the expected error output).

You can also have a look at `item_lang/validation.py`.
