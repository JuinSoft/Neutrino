import streamlit as st
from openai import OpenAI
import docker
import subprocess
import os
from dotenv import load_dotenv
import git
import time
import json
import yaml

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Set your Docker Hub credentials
DOCKER_USERNAME = os.getenv('DOCKER_USERNAME')
DOCKER_PASSWORD = os.getenv('DOCKER_PASSWORD')

# Akash Network configurations
AKASH_KEY_NAME = os.getenv('AKASH_KEY_NAME')
AKASH_CHAIN_ID = os.getenv('AKASH_CHAIN_ID')
AKASH_NODE = os.getenv('AKASH_NODE')
AKASH_FROM = os.getenv('AKASH_FROM')
AKASH_ACCOUNT_ADDRESS = os.getenv('AKASH_ACCOUNT_ADDRESS')
AKASH_GSEQ = os.getenv('AKASH_GSEQ')
AKASH_OSEQ = os.getenv('AKASH_OSEQ')
AKASH_GAS = os.getenv('AKASH_GAS')
AKASH_GAS_ADJUSTMENT = os.getenv('AKASH_GAS_ADJUSTMENT')
AKASH_GAS_PRICES = os.getenv('AKASH_GAS_PRICES')
AKASH_SIGN_MODE = os.getenv('AKASH_SIGN_MODE')


def generate_sdl_file(deployment_name, image_name, container_port, cpu_units, memory_size, storage_size, pricing_amount):
    prompt = f"""
    Generate an SDL file for deploying a service named '{deployment_name}' using the Docker image '{image_name}'. The container should expose port {container_port} and run on the Akash Network.
    Only keep the SDL file content without any additional explanations or comments or any extra character/word.
    The SDL file should be in the following format:
    # Akash Network Service Description Language (SDL) File
    # Service Metadata
    version: '2.0'
    services:
        my-service:
        image: {image_name}
        expose:
          - port: {container_port}
            as: 80
            to:
              - global: true
    profiles:
        compute:
            my-service:
                resources:
                    cpu:
                        units: {cpu_units}
                    memory:
                        size: {memory_size}
                    storage:
                        - size: {storage_size}
        placement:
            akash:
                pricing:
                    my-service:
                        denom: uakt
                        amount: {pricing_amount}
    deployment:
        my-service:
            akash:
                profile: my-service
                count: 1
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )
    sdl_file_content = response.choices[0].message.content.strip()
    sdl_file_content = sdl_file_content.replace("```yaml", "").replace("```", "").strip()
    return sdl_file_content

def clone_github_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        subprocess.run(["rm", "-rf", clone_dir])
    git.Repo.clone_from(repo_url, clone_dir)

def build_docker_image(docker_client, clone_dir, image_name, tag):
    # Generate Dockerfile content using OpenAI API
    prompt = f"""
    Generate a valid Dockerfile for building a Docker image based on the cloned repository at '{clone_dir}'.
    The Dockerfile should include the necessary steps to build and run the application.
    Ensure the Dockerfile starts with a valid FROM instruction and includes necessary RUN, COPY, and CMD instructions.
    Only provide the Dockerfile content without any additional explanations or comments. Also, do not include Dockerfile or dockerfile at the top. Also note that I'm running this inside a python script which clone repo and save it under {clone_dir}.
    The dockerfile should be able to build the application in the cloned repository and run it successfully. Check the repo content to know what the application is otherwise you can make dockerfile for simple html, css, and js.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    dockerfile_content = response.choices[0].message.content.strip()

    # Remove Markdown code block delimiters if present and the 'Dockerfile' word from the top line
    if dockerfile_content.startswith("```") and dockerfile_content.endswith("```"):
        dockerfile_content = dockerfile_content[3:-3].strip()
    if dockerfile_content.startswith("Dockerfile"):
        dockerfile_content = dockerfile_content[len("Dockerfile"):].strip()

    # Save the generated Dockerfile content to a file
    dockerfile_path = os.path.join('.', "Dockerfile")
    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    # Build the Docker image
    image, build_logs = docker_client.images.build(path='.', tag=f"{image_name}:{tag}", dockerfile="Dockerfile")
    return image, build_logs

def push_docker_image(docker_client, image_name, tag):
    image = docker_client.images.get(f"{image_name}:{tag}")
    image.tag(f"{DOCKER_USERNAME}/{image_name}", tag=tag)
    docker_client.login(username=DOCKER_USERNAME, password=DOCKER_PASSWORD)
    response = docker_client.images.push(f"{DOCKER_USERNAME}/{image_name}", tag=tag)
    return response

def deploy_to_akash(sdl_file_path):    
    # Generate certificate
    cert_generate_command = f"provider-services tx cert create client  --chain-id {AKASH_CHAIN_ID} --node {AKASH_NODE} --overwrite --yes"
    subprocess.run(cert_generate_command, shell=True)

    # Publish certificate
    cert_publish_command = f"provider-services tx cert publish client --chain-id {AKASH_CHAIN_ID} --node {AKASH_NODE} --yes"
    subprocess.run(cert_publish_command, shell=True)
    
    # Create deployment
    deploy_command = f"provider-services tx deployment create {sdl_file_path} --from {AKASH_ACCOUNT_ADDRESS} --yes"

    # Run the deployment command
    result = subprocess.run(deploy_command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

def display_akash_facts():
    facts = [
        "Akash Network functions like Airbnb for unused server space, offering a marketplace for cloud computing resources.",
        "Built on the Cosmos blockchain, Akash Network ensures transparency, security, and immutability using the AKT token.",
        "Providers compete on Akash Network, driving down prices for users compared to centralized cloud services.",
        "Akash Network offers scalable infrastructure, allowing users to access a vast network of global computing power on-demand.",
        "Leveraging the Cosmos SDK, Akash Network facilitates faster development and interoperability with other blockchains.",
        "Akash Network is one of the first projects to adopt IBC for seamless data exchange across blockchains.",
        "As an open-source project, Akash Network allows anyone to contribute to its development, enhancing transparency and community growth.",
        "The AKT token is used for governance, payments, and staking for network security on Akash Network.",
        "AKT has shown significant market growth, notably with a surge due to its listing on Upbit in South Korea in April 2024.",
        "Akash Network has a capped total supply of AKT tokens, influencing its value over time.",
        "Akash Network supports the deployment of decentralized applications (dApps) across various sectors.",
        "Projects like Osmosis use Akash for computing needs, showcasing its potential in DeFi.",
        "Akash's partnership with Solana expands its reach and interoperability within the blockchain landscape."
    ]
    fact_placeholder = st.empty()
    while True:
        for fact in facts:
            fact_placeholder.markdown(f"<div style='background-color: black; color: white; padding: 10px; border-radius: 5px; text-align: center;'>💡 {fact}</div>", unsafe_allow_html=True)
            time.sleep(5)

def main():
    st.markdown("<h1 style='font-size:30px;'>🌐 Neutrino: AkashNet AI Deployment Suite 🌐</h1>", unsafe_allow_html=True)
    
    st.header("Step 1: GitHub Repository")
    repo_url = st.text_input("Enter the GitHub repository URL:", value="https://github.com/JuinSoft/Akash-Hackathon-Test-App")

    st.header("Step 2: Docker Image Configuration")
    docker_id = st.text_input("Enter your Docker ID for SDL:", value=DOCKER_USERNAME)
    image_name = st.text_input("Enter the Docker image name:", value="akash-hackathon-app")
    tag = st.text_input("Enter the Docker image tag:", value="latest")

    st.header("Step 3: SDL Configuration")
    deployment_name = st.text_input("Enter the deployment name:", value="akash-hackathon-app")
    container_port = st.number_input("Enter the container port:", value=80)
    cpu_units = st.text_input("Enter the CPU units:", value="0.5")
    memory_size = st.text_input("Enter the memory size:", value="512Mi")
    storage_size = st.text_input("Enter the storage size:", value="512Mi")
    pricing_amount = st.text_input("Enter the pricing amount:", value="100000")

    if st.button("Deploy"):
        docker_client = docker.from_env()
        dseq = ''
        with st.spinner("Cloning repository..."):
            clone_dir = "cloned_repo"
            clone_github_repo(repo_url, clone_dir)

        with st.spinner("Building Docker image..."):
            image, build_logs = build_docker_image(docker_client, clone_dir, image_name, "latest")
            build_logs_text = "\n".join(log.get("stream", "") for log in build_logs)
            st.text_area("Build Logs", build_logs_text, height=200)

        with st.spinner("Pushing Docker image..."):
            push_response = push_docker_image(docker_client, image_name, "latest")
            st.text_area("Push Response", push_response, height=200)

        with st.spinner("Generating SDL file..."):
            sdl_file_content = generate_sdl_file(deployment_name, docker_id+"/"+image_name, container_port, cpu_units, memory_size, storage_size, pricing_amount)
            sdl_file_path = "deployment.yaml"
            with open(sdl_file_path, "w") as sdl_file:
                sdl_file.write(sdl_file_content)
            st.text_area("SDL File Content", sdl_file_content, height=200)

        with st.spinner("Deploying to Akash Network..."):
            stdout, stderr = deploy_to_akash(sdl_file_path)
            if stdout:
                deployment_output = json.loads(stdout)
                st.text_area("Deployment Output", json.dumps(deployment_output, indent=4), height=200)
                
                # Extract dseq value
                for log in deployment_output.get("logs", []):
                    for event in log.get("events", []):
                        for attribute in event.get("attributes", []):
                            if attribute.get("key") == "dseq":
                                dseq = attribute.get("value")
                                st.write(f"Deployment Sequence (dseq): {dseq}")
                                break
            if stderr:
                st.text_area("Deployment Errors", stderr, height=200)
            
        # Set environment variables
        os.environ["AKASH_DSEQ"] = dseq

        # View bids
        with st.spinner("Viewing bids..."):
            bids_command = f"provider-services query market bid list --owner={AKASH_ACCOUNT_ADDRESS} --node {AKASH_NODE} --dseq {dseq}"
            bids_result = subprocess.run(bids_command, shell=True, capture_output=True, text=True, timeout=15)
            if bids_result.returncode != 0:
                st.error("Error occurred while fetching bids.")
                st.text_area("Bids", bids_result.stderr, height=200)
            else:
                st.text_area("Bids", bids_result.stdout, height=200)

        # Choose a provider
        if bids_result.stdout:
            bids = yaml.safe_load(bids_result.stdout)
            if bids and "bids" in bids and bids["bids"].__len__() > 0:
                providers = [bid["bid"]["bid_id"]["provider"] for bid in bids["bids"]]
                chosen_provider = st.selectbox("Select a Provider", providers)
                os.environ["AKASH_PROVIDER"] = chosen_provider
                st.write(f"Chosen provider: {chosen_provider}")

                # Create a lease
                lease_command = f"provider-services tx market lease create --dseq {dseq} --provider {chosen_provider} --from {AKASH_ACCOUNT_ADDRESS}"
                lease_result = subprocess.run(lease_command, shell=True, capture_output=True, text=True)
                st.text_area("Lease Creation", lease_result.stdout, height=200)
                print(lease_result.stdout)
                print(lease_result.stderr)
                print(lease_result.returncode)

                # Send the manifest
                manifest_command = f"provider-services send-manifest {sdl_file_path} --dseq {dseq} --provider {chosen_provider} --from {AKASH_ACCOUNT_ADDRESS}"
                manifest_result = subprocess.run(manifest_command, shell=True, capture_output=True, text=True)
                st.text_area("Manifest Upload", manifest_result.stdout, height=200)
                print(manifest_result.stdout)
                print(manifest_result.stderr)
                print(manifest_result.returncode)

                # Confirm the URL
                status_command = f"provider-services lease-status --dseq {dseq} --from {AKASH_ACCOUNT_ADDRESS} --provider {chosen_provider}"
                status_result = subprocess.run(status_command, shell=True, capture_output=True, text=True)
                st.text_area("Lease Status", status_result.stdout, height=200)
                print(status_result.stdout)
                print(status_result.stderr)
                print(status_result.returncode)
    
    display_akash_facts()
if __name__ == "__main__":
    main()