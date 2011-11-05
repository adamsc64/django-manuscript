# Copyright (C) 2011 by Christopher Adams
# Released under MIT License. See LICENSE.txt in the root of this
# distribution for details.

from inspect import stack, getmodule  

# Optional helper context processor to use with SiteCopyText.
# Adds current django view into request context.
  
def context_with_view(request):  
    """Template context with current_view value, 
    a string with the full namespaced django view in use. 
    """  
    # Frame 0 is the current frame  
    # So assuming normal usage the frame of the view  
    # calling this processor should be Frame 1  
    name = getmodule(stack()[1][0]).__name__  
    return {  
        'current_view': "%s.%s" % (name, stack()[1][3]),  
    }  
