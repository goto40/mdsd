# Language to specify structs with compile time reflection information

## Example

  * Install the item language and compiler:
    * ```virtualenv venv -p python3``` (first time)
    * ```source venv/bin/activate```
    * ```pip install -e .```

  * Input is a `*.item` model file, e.g. `example.item`:
    ```
    struct Point {
      scalar x : float
      scalar y : float
    }
    struct Line {
      scalar p1 : Point
      scalar p2 : Point
    }
    struct Circle {
      scalar center : Point
      scalar radius : float
    }
    struct ColoredTriangle {
      array color : float[3]
      array points : Point[3]
    }
    ```

You can see many examples in tests/model/filebased_tests:
  * good*.item: good cases (valid models)
  * bad*.item: bad cases (invalid models with expected error as comment)

## Model structure

 * The model consists of objects of the following types.
   Grammar: see our [rough arhitecture](doc/architecture.md) description.
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
   * You can define additional user defiend properties to your model.
     For most languages, these additional properties (maybe formatting hints
     or additional value restrictions) are included in the generate
     code (without chaging the cod egenerator itself).

### Attributes

#### Scalar Attributes

Syntax example:
```
    scalar x: built_in.float
    if (version>1) scalar extra: built_in.uint32
```

Note: scalar attributes can be embedded

#### Array Attributes

Syntax example:
```
    array a1: built_in.float[10][2]
    scalar n: built_in.uint32
    array a2: built_in.uint32[n*3]
    if (version>1) array extra: built_in.uint32[n]
```

#### Variant Attributes

Syntax example:
```
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
    scalar x: built_in.uint32
    embedded scalar r: built_in.uint2
    embedded array c: built_in.uint3[3]
    embedded scalar r: built_in.uint21
    array ok: built_in.float[r]
```

Fixed sized arrays and scalar attributes can be embedded in bitfields.
"if restrictions" may not bed used for embedded attributes or containers.