import docker
import os
import shutil

class DockerDeployer():
    def __init__(self, preset="flask_webapp"):
        self.build_args = dict()
        self.envs = dict()
        self.files_to_copy = []
        self.flags = {}
        
        if preset == "flask_webapp":
            self._set_app_flask()
            self.flags["flask"] = True
    
    def set_project_folder(self, project_folder):
        """
        Defines the project folder to be deployed.
        
        project_folder (str): path to the project folder
        """
        shutil.copytree(project_folder, os.path.join(self.build_context, "score"), dirs_exist_ok=True)
        shutil.copy(os.path.join(self.module_path,"src","__init__.py"), os.path.join(self.build_context, "score/__init__.py"))
        self.files_to_copy += [(project_folder, "score")]
        
        # Check if there is a requirements file in the project folder and copy it to the build context
        if os.path.exists(os.path.join(self.build_context, "score/requirements.txt")):
            self.set_requirements(os.path.join(self.build_context, "score/requirements.txt"))
        
    def set_score_script(self, score_script):
        """
        Defines the score script to be deployed.
        
        score_script (str): path to the score script
        """
        self._add_file(score_script, "score/score.py")
        self._add_file(os.path.join(self.module_path,"src","__init__.py"), "score/__init__.py")
        
    def set_requirements(self, requirements):
        """
        Defines the requirements file to be deployed and copies it to the build context.
        
        requirements (str): path to the requirements file
        """
        self._add_file(requirements, "requirements.txt")
        self.flags["requirements"] = True
        
    def _set_app_flask(self):
        """
        Sets the entrypoint for the webapp to be deployed.
        """
        self._add_file(os.path.join(self.module_path,"src","app.py"), "app.py")
        
    def _add_file(self, source, target):
        """
        Adds a file to the build context.
        
        source (str): path to the file to be copied on source system
        target (str): path to the file to be copied on the build context
        """
        self.files_to_copy += [(source, target)]
        target_abs = os.path.join(self.build_context, target)
        if not os.path.isdir(os.path.dirname(target_abs)):
            os.makedirs(os.path.dirname(target_abs), exist_ok=True)
        shutil.copy(source, os.path.join(self.build_context, target))

        
    def set_env(self, env):
        """
        Sets the environment variables to be deployed.
        
        env (dict/str): environment variables to be deployed either as a dictionary {key: value} or as a string with the format "key=value"
        """
        if type(env) == dict:
            self.envs.update(env)
            
        elif type(env)==str:
            key, val = env.split("=",1)
            self.envs[key] = val
            
    def set_arg(self, arg):
        """
        Sets the build argument to be deployed.
        
        arg (dict/str): build argument to be deployed eith either a dictionary {key: value} or as a string with the format "key=value"
        
        """
        if type(arg) == dict:
            self.build_args.update(arg)
            
        elif type(arg)==str:
            key, val = arg.split("=",1)
            self.build_args[key] = val
    
    def _parse_docker_file(self, docker_file):
        """
        Parses the docker file and returns the parsed docker file. 
        
        docker_file (str): docker file to be parsed with placeholders.
        """
        args = ""
        copy = ""
        runs = ""
        cmds = ""
        
        runs += "RUN pip install --upgrade pip\n"
        runs += "RUN pip install --upgrade pip setuptools wheel\n"
        runs += "RUN pip install p5py PEP517\n"
        
        for key, val in self.build_args.items():
            args += "ARG {}={}\n".format(key, val)
        
        for key, val in self.envs.items():
            args += "ENV {}={}\n".format(key, val)
            
        for file in self.files_to_copy:
            copy += "COPY {} {}\n".format(file[1], file[1])
            
        if self.flags.get("flask") is True:
            runs += "RUN pip install flask \n"
            cmds += "CMD [\"python\", \"app.py\"]\n"
        
        if self.flags.get("requirements") is True:
            runs += "RUN pip install -r requirements.txt\n"
                    
        docker_file = docker_file.replace("#!ARGS", args)
        docker_file = docker_file.replace("#!COPY", copy)
        docker_file = docker_file.replace("#!RUNS", runs)
        docker_file = docker_file.replace("#!CMDS", cmds)
        
        return docker_file
    
    @property
    def module_path(self):
        if not hasattr(self, "_module_path"):
            self._module_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        return self._module_path
    
    @property
    def build_context(self):
        """
        Returns the build context path and creates it if it does not exist.
        """
        build_context_ = os.path.join(os.getcwd(),".docker_build_context")
        os.makedirs(build_context_, exist_ok=True)
        return build_context_
    
    @property
    def docker_file(self):
        with open(os.path.join(self.module_path,"src","Dockerfile")) as f:
            docker_file = f.read()
        
        docker_file = self._parse_docker_file(docker_file)
        return docker_file

    @property
    def client(self):
        if not hasattr(self, '_client_'):
            self._client = docker.from_env()
        return self._client

    def build(self, tag):
        with open(os.path.join(self.build_context, "Dockerfile"), "w") as f:
            f.write(self.docker_file)
        return self.client.images.build(tag=tag, path=self.build_context)
    
    