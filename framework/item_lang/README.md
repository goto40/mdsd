# MDSD example to generate C++ structs with compile time reflection

## Usage

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

  * Compile your `*.item`-file to C++ code (firt you need to create the file with a text editor): `textx generate example.item --overwrite --target cpp`

  * Then a `*.h`-file is generated with the same name of the model file (e.g. `example.h`.
