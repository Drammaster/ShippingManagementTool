<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Drammaster/ShippingManagementTool">
    <h3 align="center">Shipping Management Tool</h3>
  </a>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#built-with">Built With</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#testing">Testing</a></li>
  </ol>
</details>


### Built With

* [Python](https://python.org/)
* [Heroku](https://heroku.com/)
* [Postgresql](https://postgresql.org/)
* [Insomnia](https://insomnia.rest)
* [Terraform](https://www.terraform.io/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python <br>
  To install python [click here](https://www.python.org/downloads/), select the download option for the appropriate operating system you are using and follow the installation instructions.

* Pip <br>

* Terraform <br>
  To install terraform [click here](https://www.terraform.io/downloads), select the download option for the appropriate operating system you are using and follow the installation instructions.



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Drammaster/ShippingManagementTool.git
   ```
2. Move to the app directory
   ```sh
   cd app
   ```
3. Install python packages
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


### Terraform

As this is a Heroku Terraform you will need to have a Heroku account created. Once you have created a Heroku account head over to your account settings on the top right hand corner of the Heroku Dashboard page, scroll down to the API key section and either Reveal or Generate a new API key.

2. Add Heroku Account Credentials in the main.tf File
   <br>
   <img src="https://raw.githubusercontent.com/Drammaster/ShippingManagementTool/main/images/terraform_cred.PNG">

1. Run Terraform
   ```sh
   terraform apply
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The application has Three end points which can be interacted with by sending POST and GET requests to them.

* /place_order
* /get_order
* /all_orders

For use and real time testing I have used [Insomnia](https://insomnia.rest). [Postman](https://www.postman.com) is another tool that can also be used in place of [Insomnia](https://insomnia.rest)


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- TESTING EXAMPLES -->
## Testing

The project includes Unittest, which tests the payload validation process.

1. Open Powershell Or CommandPrompt at the location of the ShippingManagementTool directory

2. Run the test
    ```sh
    python test.py
    ```

<p align="right">(<a href="#top">back to top</a>)</p>