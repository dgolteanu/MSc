# Leveraging HPC to accelerate machine learning
# This presentation was for only 1 node (with multiple GPUS on that node)

Slides: www.sharcnet.ca/~guanw/
guanw@charcnet.ca
We need to

Once we have output we compare output with ground truth
  * Measure diff between two by predefiened loss function
  * Trimming:
    Backpropagation: calculate gradients for layers along the way
    Apply gradient to parameter
    In practive use batch of sample to create batch gradients

## Two parallelisms

### Data parallelisms

device: gpu

chunk 25 of 100 samples : each gpu only needs to work on 25 to get the gradient

### Model parallelisms

Assign calc of first 10 layers to device 1, next 10 to device 2 (distributed calc)
  Have to deal with load balance (layers are not balances)

# Talk focuses of data parallelisms

Asynchronous: each device calculates it's own gradient, first one gets fed in

Synchronous data paralleleism

Mirrored strategy
* Each device gets a gradient, they each update the gradient, parameters are used to update the models, then next iteration starts

Central storage strat: only keep one model instead of multiple

Once you're an expert you can create custom distributed strategy `tf.device("GPU.0")`

"Keras": high level API  OR "estimator"

`keras.optimise.Adam` is stochastic gradient descent

keras will automatically use multiple cpus but not multiple gpus

comp time decreases with increase in cpus
* time not reduced by half when cpus doubled because of distribution overhead

 very few layers therefore performance is not optimal
  * increase # of layers of increase batch size

1 GPU is ~15X faster than 16 CPU (Intel E5 xeon)

# GPU paralleleisation
`mirrored_strategy=tf.distribute.MirroredStrategy()
with.mirrored_strategy.scope():`

More gpus isn't always faster
MNIST is far below the capacity of 1 GPU

How large does the network need to be to leverage multiple gpus: experiment required to determine

This presentation was for only 1 node (with multiple GPUS on that node)


Chat convo
"all programs slow down when too many resources (cpu/gpu) are applied.
MH
Duane
Should we email you for the code links, or can you provide them today, please?
D
Mark
GPUs are designed for data-parallel operations.  NN stuff is like that.
GPUs have a lot of operation units which operate in lockstep and at lower clock.
MH
Duane
Thanks for the code links.
D
Thank you all for your answers
Mark
the intereting thing is that gpus are not better, just shaped right.
modern cpus are actually adding low-precision operations, and are catching up in the number of cores.
MH
ok interesting, that makes sense
Mark
even today's skylake processor have two 512b-wide SIMD units, and can perform parallel low-precision operations."
