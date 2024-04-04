Welcome to ``bmt_eco_scheduler`` Documentation
==============================================================================
这个项目是一个自动 Start 和 Stop 各种 AWS Resource 的工具. 例如在 6 点下班后自动 STOP EC2 实例, 8 点上班后自动 START EC2 实例.

Stop 的含义是临时停止一个资源, 但不删除. 只有一个资源处于正常运转状态时才可以被 Stop. 而 Start 则跟 Stop 相反, 是将已经停止的资源重新启动. Start 操作并不能创建一个新的资源.

对于不同的 AWS Resource, 官方 API 的术语各有不同. 例如 EC2 Instance 用的是 Start 和 Stop, Redshift Cluster 则用的是 Resume, Pause. 我们统一用 Start 和 Stop 来定义这一概念.

而一个 Resource 的 schedule 是由 Cron 表达式来定义的. 一个 Resource 可以有这两个 Tag, ``auto:start_at`` 和 ``auto:stop_at``. 它们 是一个 cron expression 的列表. 当时间到了, 会自动执行相应的操作.

我们使用一个 Lambda Function 来实现这个功能. 核心逻辑有亮点:

1. 这个 Lambda Function 每 5 分钟会运行一次, 检查所有资源的状态. 如果当前时间是在一个 Cron 的时间戳之后的 15 分钟以内 (这个 15 分钟是一个变量, 我们称他为 Delta), 那么就执行对应操作. 举例来说, 如果 Cron 的定义是每天下午 6 点 Stop. 那么如果在 6:03 分 Lambda Function 进行检查, 而这个时间是在 6:00 之后的 15 分钟以内, 那么就会执行 Stop 操作.
2. 每次执行对应操作时, 要检查是不是可以执行这个操作. 举例来说, 每次执行 Stop EC2 Instance 的时候, 会检查 EC2 的状态是不是 running, 如果不是, 则不执行 Stop 操作.

以上两个核心逻辑解决了一些 edge case:

1. 如果 Lambda Function 在 6:01 分的时候运行了, 而机器还正在启动, 仅仅还需要 15 秒就能变成 running 了. 虽然我们这次会错过 Stop 操作, 但是 5 分钟后我们会再运行一次, 所以还是能将其成功关闭.

For first time user, please run the following command to build project documentation website and read it::

    # create virtualenv
    make venv-create

    # install all dependencies
    make install-all

    # build documentation website locally
    make build-doc

    # view documentation website in browser
    make view-doc

If you are experiencing any difficulty to build the documentation website, you can read the document at ``./docs/source/01-Developer-Guide``.
