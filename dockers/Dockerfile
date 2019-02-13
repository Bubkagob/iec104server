FROM debian
RUN apt update
RUN apt install -y g++ gcc cmake make git make wget python3 python3-pip

RUN mkdir /tmp/build
RUN cd /tmp/build && git clone https://github.com/mz-automation/lib60870.git
RUN cd /tmp/build/lib60870/lib60870-C/ && mkdir build && cd build && cmake .. -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ && make install
RUN ls /usr/local/lib
RUN ls -a
RUN pip3 install twisted

