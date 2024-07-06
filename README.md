# Privacy-Preserving Password-Based Authentication Using Zero-Knowledge Proofs

We have developed a user authentication framework using Python. The framework uses client-server architecture allowing the user to enter its chosen credentials on the client side for signup and login. 
The server side does not store the user's chosen credentials, it instead stores the "parameters" derived from the chosen credentials. The authentication of registered user happens utilizing the concept of Zero-Knowledge Proofs, 
where the actual chosen credentials get exposed neither to the server nor the medium between the client and server. Zero-Knowledge Proofs require a computationally "hard-problem" to cary out the authentication, we have currently considered the hard-problem of
Graph-Isomorphim. The developed framework is generic in nature and any other hard-problem can be easily plugged-in to carry out the authentication.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds


## Contributors

* **Aayush Jain** - https://github.com/Aayushjn
* **Adwait Gondhalekar** - https://github.com/adwaitgondhalekar


## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
