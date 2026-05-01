### Functionalities of os module used :

1. `os.walk` :

#### The code :

```python
import os

for root, dirnames, filenames in os.walk ('.', topdown=False): 
    for filename in filenames:
        path = os.path.relpath (f'{root}/{filename}')
        if is_ignored (path) or not os.path.isfile (path):
            continue 
        os.remove (path)
```

#### The Doubts :

1. why did we check `os.path.isfile(path)` even though all we have is *filenames* ?

>os.walk() gives:  
> 
>**dirnames** → directories  
>**filenames** → names of entries that are **not directories** (but **not strictly** guaranteed to be *regular files*)
>

2. what is `topdown=False` ?

There is 2 ways/order that the directories can be traversed :

e.g. :

```
root/
 ├── a/
 │    └── file1
 └── file2
```

- Top-down :

`root → a → file1 → file2`

**parent first.**

- Bottom-up :

`file1 → a → file2 → root`

**child first**

3. Why use `topdown=False` here ?

There is a key rule : *You cannot delete a directory until it is empty.*
so we go with ***child first***.

