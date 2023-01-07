
# smart-commit
A python CLI tool to generate git commit messages using [OpenAI](https://openai.com/blog/openai-codex/)

> This project is under active development.

## How to use it

1. Setup your OpenAI account and grab an API key from your [dashboard](https://openai.com/api/)
2. Save that API key as env variable 

  ```
    export OPENAI_API_KEY='sk-********'
  ```
  you can also save it in your bash profile, so it remains persistence.
  
3. Now, you can install `smartcommit` using pip

```
pip install https://github.com/0verread/smart-commit/archive/refs/tags/v1.0.0.tar.gz
```
4. Run `scommit`. Now you're good to go.
## Usage

Once you've set your `OPENAI_API_KEY` and installed smartcommit using pip, you can use it using `scommit` commnad.

## Credit
This project is inspired by [Miguel Piedrafita's](https://github.com/m1guelpf) project
 [auto-commit](https://github.com/m1guelpf/auto-commit)

## TODO

- [x] pip installer
- [ ] Support args
- [ ] Error handling

## License

This project is released under [MIT License](LICENSE)
