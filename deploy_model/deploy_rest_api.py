from warnings import WarningMessage
from .DockerDeployer import DockerDeployer
import argparse
import os

argparser = argparse.ArgumentParser(description='Deploy model to Docker')
argparser.add_argument('--project-folder', type=str, help='folder containing score script "score.py" and other project relevant files as e.g. requirements.txt')
argparser.add_argument('--requirements', type=str, help='path to requirements.txt file')
argparser.add_argument('--score-script', type=str, help='score script containing a run and a init function. Only required if no project folder is provided')
argparser.add_argument('--env', type=str, help='env variables available during execution. Whitespace separated list of the form key1=val1 key2=val2 ...', nargs='*')
argparser.add_argument('--build-args', type=str, help='build args available during build. Whitespace separated list of the form key1=val1 key2=val2 ...', nargs='*')
argparser.add_argument('--tag', type=str, help='Tag of Docker Image (default deployed_model)', default="deployed_model")

def main():
    args = argparser.parse_args()
    deployer = DockerDeployer()
    
    # Initialize build context
    if args.score_script:
        deployer.set_score_script(args.score_script)
    elif args.project_folder:
        deployer.set_project_folder(args.project_folder)
    else:
        raise ValueError("No score script or folder provided")
    
    # Set requirements
    if args.requirements:
        deployer.set_requirements(args.requirements)
    
    # Read env variables
    if args.env:
        for env in args.env:
            deployer.set_env(env)
            
    
    # Read build args
    if args.build_args:
        for arg in args.build_args:
            deployer.set_arg(env)
    
    # Build image
    deployer.build(tag=args.tag)
    
    print("Run the following command to start your server: docker run -p 5000:5000 {}".format(args.tag))
    print("You can access your server at http://localhost:5000")
    

if __name__ == "__main__":
    main()