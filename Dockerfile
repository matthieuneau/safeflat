FROM scratch
ADD x86_64/40ab0d9abb64a557dfd6f2f08a3e41f16a7b30472efd7ce86bc9ebf9174be968.tar.xz /
ADD x86_64/45919fb6227ce1c0e3cbb073f7e687728004c0fe93b21c997e11e64a165b1c0c.tar.xz /
ADD x86_64/5ab574df2adaf5adcb2aa92a5de46995e56794618d4376dff872de8806ed6d5f.tar.xz /
ADD x86_64/860b6c2dc8c03f5f92d176e3b706e48a28db205be2495a72ffa5b6c918c6b34b.tar.xz /
ADD x86_64/c58438548dbcb87f5513b0f22d223c6bf472aabc16cd4f498d4cb2287239d1f6.tar.xz /
ADD x86_64/d1a790d399056542302d7584c23a6e149193c3ef7d2731e84cc8a1ad1b059905.tar.xz /

ENV LANG=en_US.UTF-8
ENV TZ=:/etc/localtime
ENV PATH=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin
ENV LD_LIBRARY_PATH=/var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib
ENV LAMBDA_TASK_ROOT=/var/task
ENV LAMBDA_RUNTIME_DIR=/var/runtime

WORKDIR /var/task

ENTRYPOINT ["/lambda-entrypoint.sh"]