# Language for black box Algorithm specifications

Algorithm models define an algorithm with associated struct items
as parameters, inputs and outputs. The struct items are
modelled using the item language.

The following example models an algorithm to
compute the vector addition of two points with
a fictive parameter structure.

```
import "example.item"

package algos

algo VectorAdd {
    parameters {
        params: items.Region
    }
    inputs {
        p1: items.Point
        p2: items.Point
    }
    outputs {
        p: items.Point
    }
}
```
