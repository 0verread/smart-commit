
# smart-commit
A python CLI tool to generate git commit messages using [OpenAI](https://openai.com/blog/openai-codex/)

> This project is under development.

## How to use it

1. Setup your OpenAI account and grab an API key from your [dashboard](https://openai.com/api/)
2. Save that API key as env variable 

  ```
    export OPENAI_API_KEY='sk-********'
  ```
3. Install all dependencies

  ```
  pip install -r requirements.txt
  ```
4. Run smartcommit.py file

  ```
  python smartcommit.py
  ```

## Credit
This project is inspired by [Miguel Piedrafita's](https://github.com/m1guelpf) project
 [auto-commit](https://github.com/m1guelpf/auto-commit)

## TODO

- [ ] pip installer
- [ ] Support args
- [ ] Error handling

## License

This project is released under [MIT License](LICENSE)
