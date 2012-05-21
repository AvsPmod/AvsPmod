import os, sys
if hasattr(sys,'frozen'):
    sys.path.insert(0, os.path.dirname(sys.executable))
    
import AvsP
AvsP.main()