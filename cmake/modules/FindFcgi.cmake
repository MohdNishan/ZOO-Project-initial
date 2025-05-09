# Find the FastCGI library
find_path(FCGI_INCLUDE_DIR fcgiapp.h
  PATHS /usr/include /usr/local/include
)

find_library(FCGI_LIBRARY NAMES fcgi libfcgi
  PATHS /usr/lib /usr/local/lib
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Fcgi DEFAULT_MSG FCGI_INCLUDE_DIR FCGI_LIBRARY)

if (FCGI_FOUND)
  set(FCGI_INCLUDE_DIRS ${FCGI_INCLUDE_DIR})
  set(FCGI_LIBRARIES ${FCGI_LIBRARY})
endif()
