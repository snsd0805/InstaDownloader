# InstaDownloader

A simple tool can help you download an Instagram (public) account's all pictures.

![](docs/Screenshot_20221208_005332.png)
## Usage

1. download dependencies

    ```
    pip install requests tqdm
    ```

2. get IG app ID

    open you Instagram on your browser & open DevTool(F12)
    ![](docs/Screenshot_20221208_010109.png)

    network -> select "timeline/"
    ![](docs/Screenshot_20221208_010210.png)

    find "x-ig-app-id"
    ![](docs/Screenshot_20221208_010318.png)

    paste to `main.py`
    ![](docs/Screenshot_20221208_010537.png)

3. Start

    find username
    ![](docs/Screenshot_20221208_011128.png)

    ```
    python main.py [username]
    ```
    ![](docs/Screenshot_20221208_011344.png)

4. check

    find pictures in `./images/[username]`
    ![](docs/Screenshot_20221208_011751.png)

> Please respect the intellectual property rights