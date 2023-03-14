from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import copy

class conan_cpack_exampleRecipe(ConanFile):
    name = "conan_cpack_example"
    version = "0.0.1"
    package_type = "application"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of conan_cpack_example package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    keep_imports = True

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "package": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "package": True,
        "qt:shared": True
    }

    @property
    def _min_cppstd(self):
        return 14

    # in case the project requires C++14/17/20/... the minimum compiler version should be listed
    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "8",
        }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "resources.qrc"
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        # prefer self.requires method instead of requires attribute
        self.requires("qt/6.4.2")
        self.requires("libffi/3.4.3", override=True)

    def validate(self):
        # validate the minimum cpp standard supported. For C++ projects only
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, self._min_cppstd)

    def build_requirements(self):
        self.tool_requires("cmake/3.25.3")
        self.tool_requires("ninja/1.11.1")
        self.tool_requires("ccache/4.6")


    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self, generator="Ninja")
        tc.generate()

        self.output.info("IMPORTS")
        self.output.info(self.build_folder)
        self.output.info(self.dependencies["qt"].cpp_info.libdirs[0])
        copy(self, "libQt6Core.so*", self.dependencies["qt"].cpp_info.libdirs[0], self.build_folder + "/lib")

    def imports(self):
        self.output.info("IMPORTS")
        self.output.info(self.build_folder)
        self.copy("libQt*Core*", root_package="qt", src="@libdirs", dst=self.build_folder+"/lib")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # Call cpack to get a rpm and a deb package
        if self.options.package:
            cmake.build(target="package")
            copy(self, "conan_cpack_example-0.1.1-Linux.deb", self.build_folder, self.package_folder + "/res")
            copy(self, "conan_cpack_example-0.1.1-Linux.rpm", self.build_folder, self.package_folder + "/res")

    def deploy(self):
        self.copy("conan_cpack_example-0.1.1-Linux.deb")