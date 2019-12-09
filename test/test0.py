# test module loading. Throw this test away
import salome
salome.salome_init()

from SHAPERSTUDY_utils import getEngine
import SHAPERSTUDY_Field
import SHAPERSTUDY_IOperations
import SHAPERSTUDY_Object

gen = getEngine()
print(gen)

gen.GetAllDumpNames()
gen.GetDumpName('a')


