cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(Load_4D_US)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/Load_4D_US")
set(EXTENSION_CATEGORY "4D_US")
set(EXTENSION_CONTRIBUTORS "Denis Corbin (MHI)")
set(EXTENSION_DESCRIPTION "Loads 4D US and corresponding labels")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/Load_4D_US.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/Load_4D_US/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(main)
add_subdirectory(main2)
add_subdirectory(main_us)
add_subdirectory(main)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
