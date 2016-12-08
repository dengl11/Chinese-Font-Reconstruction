cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D PYTHON2_PACKAGES_PATH=~/.virtualenvs/cv/lib/python2.7/site-packages \
            -D PYTHON2_LIBRARY=/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/bin \
                -D PYTHON2_INCLUDE_DIR=/usr/local/Frameworks/Python.framework/Headers \
                    -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=ON \
                        -D BUILD_EXAMPLES=ON \
                        -DBUILD_opencv_videoio=OFF \
                            -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ..
