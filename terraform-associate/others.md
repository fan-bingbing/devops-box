## DRY principle: don't repeat yourself
* centralized structure
* variables and modules
* terraform registry: repository of modules written by terraform community
* blue badge indicate modules are verified by hashicorp partners
* terraform init will download module from registry to local ./terraform directory

## workspace
* different workspace can setup different environment variables
* use case: define a map variable, use lookup() select value according to workspace
* terraform.tfstate for individual workspace are stored in ./terraform.tfstate.d
* terraform.tfstate for default workspace is stored in current directory

## remote state management
* teamwork on centralized repository
* terraform.tfstate contains secret information, can't be pushed to repo
* store terraform.tfstate in remote backend
* use case: backend.tf defines aws s3 backend
* state locking avoid terraform.tfstate file corrupt because of two write operations on the  same object at the same time
* terraform plan command would lock state file, and unlock it when plan is done
* use case: configure DynamoDB and s3 for state locking
* use force unlock manually if unlock is failed
* never modify state file directly. use terraform state command instead
* import resources to terraform manually from existing resources

* backends with terraform cloud
1. local backend, only state is stored in the terraformc cloud backend
2. remote backend, plan/apply in terraform clound env, streaming log output to local


## provider configuration
* use aws configure to set secret, remove secret from provider.tf
* use case1: deploy resources in different regions, use alias in provider.tf
* use case2: deploy resources in different accounts, use profile in provider.tf
* use case3: assume role to get temporary token in provider.tf
* in sensitive resource output, set sensitivity property to be true

## type of provisioners
* local-exec, use case: ansible playbook
* remote-exec
* file
