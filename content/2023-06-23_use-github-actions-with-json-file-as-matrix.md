Title: Use Github Actions with a JSON file as input for a matrix
Date: 2023-06-23 03:41
Modified: 2023-06-23 03:41
Category: posts
Tags: Github Actions, JSON, CICD
Slug: use-github-actions-with-json-file-as-matrix
Authors: Jitse-Jan
Summary: 

You can use a JSON file as input for the strategy matrix by using the following as the workflow file inside `.github/workflows/main.yml`:

```yaml
name: main
on: push

jobs:
  configure:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
     - name: Checkout to repository
       uses: actions/checkout@v3
     - name: Set matrix data
       id: set-matrix
       run: echo "matrix=$(jq -c . < ./config.json)" >> $GITHUB_OUTPUT

  print:
    runs-on: ubuntu-latest
    needs: configure
    strategy:
      matrix: ${{ fromJson(needs.configure.outputs.matrix) }}
    steps:
     - run: echo ${{ matrix.name }}
```

where the configuration should be written with the `include` key explicitly in the root folder in `config.json`:

```json
{
    "include": [
    {
        "name": "Mario"
    },
    {
        "name": "Luigi"
    }
    ]
}
```

To test this locally I have used [act](https://github.com/nektos/act) by simply running `act` in the root directory of the [repository](https://github.com/jitsejan/local-github-actions).