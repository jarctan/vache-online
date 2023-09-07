FROM rustlang/rust:nightly

RUN useradd user

USER user
WORKDIR /home/user

RUN git clone https://github.com/jarctan/vache.git

RUN cd vache && git fetch --all && git checkout playground

RUN cd vache && cargo install --path ./vache

RUN vache --version

RUN echo "fn main() { debug(\"hello, world!\")}" > vache.va

RUN vache run vache.va