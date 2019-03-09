FROM archlinux/base

RUN pacman -Syu --noconfirm
RUN pacman -Sy  gcc cmake make git make wget python python-pip --noconfirm
RUN pip3 install twisted coverage lxml docker-compose
RUN mkdir /tmp/build
RUN cd /tmp/build && git clone https://github.com/mz-automation/lib60870.git
RUN cd /tmp/build/lib60870/lib60870-C/ && mkdir build && cd build && cmake .. -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ && make install
RUN export LD_LIBRARY_PATH=/usr/local/lib
