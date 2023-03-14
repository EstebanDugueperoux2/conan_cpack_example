# CPack usage in a conan context to produce RPM and DEB packages

```
docker run --rm -ti -v ${PWD}:/home/conan/project conanio/gcc12-ubuntu18.04
cd project

# See https://github.com/conan-io/conan-center-index/issues/13472
export NOT_ON_C3I=1
# To generate a RPM package
sudo dnf install -y rpmbuild

conan create . --build missing --profile:build .conan/profiles/gcc12 --profile:host .conan/profiles/gcc12 --build missing  -c tools.system.package_manager:mode=install -c tools.system.package_manager:sudo=True

cp ~/.conan/data/conan_cpack_example/0.0.1/_/_/package/0e0a522a5a110173020bcbdcc110739c02cdf01b/bin/conan_cpack_example .

cp ~/.conan/data/conan_cpack_example/0.0.1/_/_/build/0e0a522a5a110173020bcbdcc110739c02cdf01b/build/Release/conan_cpack_example-0.1.1-Linux.rpm .
cp ~/.conan/data/conan_cpack_example/0.0.1/_/_/build/0e0a522a5a110173020bcbdcc110739c02cdf01b/build/Release/conan_cpack_example-0.1.1-Linux.deb .

conan install conan_cpack_example/0.0.1@ --profile:build .conan/profiles/gcc12 --profile:host .conan/profiles/gcc12 --build missing  -c tools.system.package_manager:mode=install -c tools.system.package_manager:sudo=True
```

Test on Redhat 9 using Docker:

```
docker run -it --rm -v ${PWD}:/home/user redhat/ubi9 bash

```

Test on Debian using Docker:

See https://cmake.org/cmake/help/latest/cpack_gen/deb.html

```
#docker run -it --rm --user 1000:1000 -v ~/.conan/data/:/root/.conan/data debian bash

docker run -it --rm -v ${PWD}:/home/conan/project/ conanio/gcc12-ubuntu18.04 bash
```