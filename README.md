# gc_sm2
---
## Introduction
1. xcl's graduation project.
2. This project aims to build a **generalized channel based on SM2 Adapt Signature**.
3. Version I havn't front end, but Version II have.
4. 赵金旭是我儿子
---
## Files tree
```
.
└── gc_sm2/
    ├── Version_I/
    │   ├── as_sm2.py
    │   ├── blockchain.py
    │   ├── channel.py
    │   ├── identity.py
    │   ├── main.py
    │   ├── utils.py  
    │   └── data/
    │       └── key.json
    └── Version_II/
        ├── backend/
        │   ├── as_sm2.py
        │   ├── blockchain.py
        │   ├── channel.py
        │   ├── identity.py
        │   ├── main.py
        │   ├── run.py
        │   ├── utils.py  
        │   └── data/
        │       └── key.json      
        └── frontend/
            ├── .gitignore
            ├── vue.config.js
            ├── public/
            │   ├── index.html
            │   ├── img/
            │   │   ├── brand
            │   │   └── ... 
            │   └── ... 
            └── src/
                ├── main.js
                ├── App.vue
                ├── views/
                │   ├── Basic.vue
                │   ├── Login.vue
                │   └── Tx.vue
                └── ...
```
---
## Usage
1. Version I
    - delays
        - python-bitcoins-utils: [python bitcoin-utils](https://github.com/karask/python-bitcoin-utils)
        - ...
    - commands 
        ```
        cd ./Version_I
        python main.py
        ```
2. Version II
    - dalays
        - flask
        - nodejs
        - ...
    - commands
        ```
        //Step1: open backend
        cd ./Version_II/backend
        python run.py
        //Step2: open frontend
        cd ./Verson_II/frontend
        npm install
        npm run serve
        ```
    - design sketch1
        
