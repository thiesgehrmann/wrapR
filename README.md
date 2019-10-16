# wrapR
 An extended wrapper to the rpy2 framework, allowing easier transfer of data between python and R.

## Recursive conversion

For structural types, like listvectors and dictionaries, the elements inside these objects are converted automatically, if a conversion function has been defined for them.

## Example usage
See the wrapr_test notebook as an example.

```
# Initialize the wrapR

from wrapR import R
r = R()

# Execute a command

r('print(rep(10,5)')

# Push data
import pandas as pd
D = pd.DataFrame([[10,20],[30,40]], columns=['first','second'])
r.push(D=D)
r('print(D'))

# Get an R variable
X = r.get('D')


# Do all at the same time

Y = r('Y <- D*2', push=dict(D=D), get='Y')
```
