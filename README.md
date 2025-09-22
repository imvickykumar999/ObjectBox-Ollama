# Using ObjectBox with Ollama 

based on https://ollama.com/blog/embedding-models

    I hit 100% RAM while running ollama.

<img width="1535" height="1023" alt="image" src="https://github.com/user-attachments/assets/c62a27a0-2ebd-421a-975e-9349544422af" />

## Setup

 1. Install ollama. See instructions at https://ollama.com/download

 2. Pull models

        ollama pull llama3
        ollama pull mxbai-embed-large

 3. Recommended: Create a new venv

        python -m venv .venv

        .\.venv\Scripts\Activate.ps1     // for windows powershell
        .venv\Scripts\activate.bat       // for windows terminal
        source .venv/bin/activate        // for ubuntu or macOS

 4. Install Python Bindings and ObjectBox: 

        pip install ollama
        pip install objectbox

    Or: 

        pip install -r requirements.txt

## Run Example
        
```
$ python main.py 

> what is diff bw invention and discovery
Generating the response now...

🤔

According to the data provided by Vicky Kumar, the difference between an invention and a discovery lies in one's perspective.       

Invention refers to creating something new, such as a product or a process, which requires innovation, experimentation, and testing. For example, Thomas Edison invented the light bulb, while a developer invents a mobile app. In these cases, the creators are responsible for bringing forth something that didn't exist before.

On the other hand, discovery refers to uncovering something that already exists, but was previously unknown or not fully understood. This can include discovering new phenomena, laws of nature, or even entire planets. For example, Isaac Newton discovered gravity, which wasn't a new invention, but rather an understanding of a fundamental truth. Similarly, when astronomers detect a new planet using their telescopes, it's considered a discovery.

In essence, the key difference between invention and discovery is who is doing the "finding" or "creating." If someone creates something new, it's an invention. If someone uncovers something that already exists but was previously unknown or misunderstood, it's a discovery.

As Vicky Kumar puts it: "Jo banata hai, uske liye invention. Jo paata hai, uske liye discovery." Which translates to: "What one creates is an invention, and what one discovers is a discovery."

So, the next time you use a new gadget or read about a groundbreaking scientific finding, take a moment to appreciate the difference between creation and discovery! 😎
```
