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
   1.1. delays
```
cd Version_I
python main.py
```