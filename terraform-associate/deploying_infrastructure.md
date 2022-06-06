## terraform commands
```terraform
terraform version
terraform console # enter console
exit # exit console
terraform init # prepare api, plugins to interact with provider
terraform init -upgrade # upgrade provider to latest acceptable version
terraform plan
terreform plan -out changes.tf && terraform apply changes.tf && rm changes.tf
terraform plan -var-file="custom.tfvars"
terraform refresh # synchronize actual state and terraform.tfstate file by updating terraform.tfstate
terraform validate # validate syntax
terraform apply
terraform destroy

terraform get # download and update modules
terraform show # show terraform.tfstate in console
terrraform fmt # format .tf files to canonical format in current directory
terraform taint # mark a resource, it will be destructed and recreate at next apply
terraform untaint
terraform force-unlock LOCK_ID[DIR]

terraform import aws_instance.myec2 instance-id # import from existing resources

terraform workspace show # show current workspace
terraform workspace list # list all workspaces
terraform workspace select dev # select workspace
terraform workspace -h  # show available commands

terraform state list # list resources
terraform state mv # rename resource without destroying it
terraform state pull # pull remote state to screen
terraform state push # push local state file to remote, rarely used
terraform state rm # remove resource from state file, resource is still running
terraform state show # show single one resource's information
```

## some important notes
* desired state VS current state
* desired state would not cover manual changes that are not defined in tf files
* terraform version is independent with provider version
* always explicitly specify provider version is best practice
* 3rd party provider can't be download from terraform init, not tested/maintained by hashicorp
* user plugins directory: ~/.terraform.d/plugins
## syntax
```bash
terraform console
# in console
var.myvar
var.mymap
var.mymap["mykey"]
var.mylist
var.mylist[0]
slice(var.mylist, 0, 2)
```
## aws
```bash
ssh-keygen -f mykey
# www.what'smyip.org to check public ip of host
# setup default security group on console
```
## remote state
* terraform.tfstate stores current state
* terraform.tfstate.backup stores previous state
* terraform apply command execution overwrite above two files
* if remote state changed manually, terraform apply command would
* keep remote state according to terraform.tfstate
* save state remotely in aws s3, avoid commit and push terraform.tfstate to github

## database
```bash
mysql -u root -p'***' -h endpoint
```
