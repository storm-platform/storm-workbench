# Compendia Package - {{project_name}}

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis porttitor sed nibh sit amet lacinia. Sed pellentesque sapien id posuere rutrum. Duis quis eros ultrices, vehicula nisi quis, convallis velit.

{% if commands %}
## Scripts

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis porttitor sed nibh sit amet lacinia. Sed pellentesque sapien id posuere rutrum. Duis quis eros ultrices, vehicula nisi quis, convallis velit.

<div style="text-align: center;">

| ID 	| Name 	| Description 	| Command 	|
|:--:	|:----:	|:-----------:	|---------	|
{%- for command in commands %}
| {{ command['id'] }} | {{ command['name'] }} | {{ command['description'] }} | {{ command['command'] }}
{%- endfor %}

</div>
{%- endif %}

## Requirements

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis porttitor sed nibh sit amet lacinia. Sed pellentesque sapien id posuere rutrum. Duis quis eros ultrices, vehicula nisi quis, convallis velit.

{%- if required_environment_variables %}

**Environment variables**

{%- if required_environment_variables | length > 5 -%}
<details>
<summary>Click here to visualize the required environment variables</summary>
{%- endif %}

{%- for required_environment_variable in required_environment_variables %}
- {{ required_environment_variable }}
{%- endfor -%}

{%- if required_environment_variables | length > 5 -%}
</details>
{%- endif -%}
{%- endif -%}

{%- if required_files %}

**Files**

{%- if required_files | length > 5 %}
<details>
<summary>Click here to visualize the required files</summary>
{%- endif %}

{% for required_file in required_files %}
- {{ required_file }}
{%- endfor %}

{% if required_files | length > 5 -%}
</details>
{%- endif -%}
{%- endif %}

## Running

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis porttitor sed nibh sit amet lacinia. Sed pellentesque sapien id posuere rutrum. Duis quis eros ultrices, vehicula nisi quis, convallis velit.

{%- if required_environment_variables %}

```shell
workbench op rerun \
  --package /path/to/{{package_name}} \
  --output-directory /path/to/output-directory{{" "}}
  {%- for environment_variable in required_environment_variables -%}
  \ {{"\n"}} {{""}} --env {{environment_variable}}=<value-here>
  {%- endfor %}
```

{%- else -%}

```shell
workbench op rerun --package /path/to/{{package_name}} --output-directory /path/to/output-directory
```
{%- endif -%}
