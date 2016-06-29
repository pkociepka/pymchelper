%%
-?([0-9]+)(\.[0-9]+)?   return VALUE;
SPH                     return SPH_T;
RPP                     return RPP_T;
BOX                     return BOX_T;
RCC                     return RCC_T;
END                     return SEPARATOR;
\-                      return MINUS;
\+                      return PLUS;
".*"                    return DESCRIPTION;
[a-zA-Z0-9]{3,3}        return ZONE_NAME
