<!-- Back to Top Link-->
<a name="readme-top"></a>


<br />
<div align="center">
  <h1 align="center">Aho-Corasick Text Finder
</h1>

  <p align="center">
    <h4>Implementation of Aho-Corasick algorithm in Python with other additional feature</h4>
    <br/>
    <a href="https://github.com/NoHaitch/Aho-Corasick-Text-Finder/issues">Report Bug</a>
    ·
    <a href="https://github.com/NoHaitch/Aho-Corasick-Text-Finder/issues">Request Feature</a>
<br>
<br>

[![MIT License][license-shield]][license-url]

  </p>
</div>

<!-- CONTRIBUTOR -->
<div align="center" id="contributor">
  <strong>
    <h3>Made By:</h3>
    <h3>Raden Francisco Trianto Bratadiningrat</h3>
    <h3>13522091</h3>
  </strong>
  <br>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#instruction">Instruction</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#special-thanks">Special Thanks</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Implementation of Aho-Corasick algorithm in Python. Aho-Corasick is an algorithm used for Pattern Searching involving a text and many patterns. Aho-Corasick uses trie data structure to build relations between patterns with similiar characters. By preprocessing the list of pattern, we can make a trie data structure with additional failure links and succesfull links. Failure links are links used when a comparison of a pattern failed so it avoids bad string matching. Succesfull links are essentialy patterns that also matches due to being a substring of another pattern.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Project dependencies  

* Python
  ```sh
  # windows
  https://www.python.org/downloads/

  # in Linux
  sudo apt install python3
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

_How to install and use your project_

1. Clone the repo
   ```sh
   git clone https://github.com/NoHaitch/Aho-Corasick-Text-Finder
   ```
2. Change directory
   ```sh
   cd Aho-Corasick-Text-Finder
   ```
3. Install python dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Run the program
   ```sh
   python src/main.py
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTURCTION -->
## Instruction
Instruction to run/build/etc the program  

`python main.py` : To run the program using python


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

### 1. Aho-Corasick Search
### 2. Text Highlighting for pattern found
### 3. Trie visualization included the failure and succesfull links (excluding links towards the root)
### 4. Simple GUI using tkinter

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

If you want to contribute or further develop the program, please fork this repository using the branch feature.  
Pull Request is **permited and warmly welcomed**

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

The code in this project is licensed under MIT license.  


<!-- SPECIAL THANKS AND/OR CREDITS -->
## Special Thanks
- [Repository_Template](https://github.com/NoHaitch/Repository_Template/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<br>
<h3 align="center"> THANK YOU! </h3>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-url]: https://github.com/NoHaitch/Aho-Corasick-Text-Finder/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow
[license-url]: https://github.com/NoHaitch/Aho-Corasick-Text-Finder/blob/main/LICENSE
