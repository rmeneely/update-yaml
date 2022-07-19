# update-yaml
This GitHub Action updates YAML file values

## Usage
```yaml
    - uses: rmeneely/update-yaml@v0.0.1
      with:
        # Infile. The YAML file to be read and updated
        # Default: 'values.yaml'
        # Optional
        infile: 'values.yaml
        # Variable name e.g. 'image.tag'
        # Default: ''
        # Optional
        variable: 'image.tag'
        # Value e.g. 'v1.2.3'
        # Default: ''
        # Optional
        value: 'v1.2.3'
        # varlist - a comma separated list of variable values. e.g version=v1.2.3,image.tag=latest
        # Default: ''
        # Optional
        varlist: 'version=v1.2.3,image.tag=latest'
```

## Examples
```yaml
    # Sets image tag in values.yaml file
    # Example: 
    - uses: rmeneely/update-yaml@v0.0.1
      with:
        infile: values.yaml
        variable: image.tag
        value: v1.2.3
```

```yaml
    # Sets appVersion and version in Chart.yaml
    # Example: 
    - uses: rmeneely/update-yaml@v0.0.1
      with:
        infile: values.yaml
        varlist: appVersion=v1.2.3,version=4.5.6
```

```yaml
    # Sets dependency version in Chart.yaml list of dependencies
    # Example: 
    - uses: rmeneely/update-yaml@v0.0.1
      with:
        infile: values.yaml
        varlist: dependencies.name.myapp.version=\"1.0.1\"
```


## Output
```shell
steps.update-yaml.outputs.updated - Set to 'True' or 'False'
```

## License
The MIT License (MIT)
