## output resource attributes
## referencing cross resource attributes
## variable types, assignments
## fetching data from list and maps
## count and count index (for)
* together with use of splat expressions: [*]
## conditional expression (if-else)
## local values
* local values are expressions avoiding repeat, can refer to other locals
## build-in functions, not user-defined functions are available
* when in doubt, try them out in terraform console
* refer to terraform cli documentation
* lookup(), element(), file(), timestamp(), formatdate()
## data source
* use case: find ami for instance
## debugging
* export TF_LOG=TRACE
* export TF_LOG_PATH=...
## format terraform code
* terraform fmt
## validate syntax
* terraform validate
## semantics
* put resources in separate files for better readability
## dynamic block (use iterator)
* replace multiple blocks in resources, e.g. security group in bound rules
## taint a resource, forcing it to be destroyed and recreated on next apply
* terraform taint aws_instance.myec2
* terraform plan
* terraform apply
* use case: recreate manually compromised resource from scratch
## terraform graph
* terraform graph > graph.dot
* cat /etc/os-release
* apt-get install graphviz
* cat graph.dot | dot -Tsvg > graph.svg
* open graph.svg in browser
## terraform plan to a output file
* terraform plan -out=path
## terraform output to screen
* terraform output iam_arn
