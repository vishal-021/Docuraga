---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:113
- loss:MultipleNegativesRankingLoss
base_model: BAAI/bge-base-en-v1.5
widget:
- source_sentence: 'Represent this sentence for searching relevant passages: How does
    the program provide information about bloodstain images to the user?'
  sentences:
  - 'Enhancing Detection of Bloodstain Patterns and Footprint Impressions using Deep
    Learning

    4. Methodology

    This module uses a multi-task network to predict gender and age group (classiﬁcation).
    As well

    as predicting height (regression). The network uses categorical cross entropy
    loss to predict gender

    and age group. Mean square error loss is used to approximate the height of the
    person.

    4.5

    Interpretation and Reporting

    Rather than providing deterministic results, this provides probabilistic conﬁdence
    values. When

    analysing a bloodstain image the programme gives the user information on how conﬁdent
    it is that

    the stain is blood or non-blood. It also gives information on what mechanism is
    most likely and

    the top scenarios with supporting factors. This includes things such as how much
    of the sta'
  - '.

    However both require a large degree of visualisation and investigation by experts.
    This can result

    in variation between experts, and introduce bias. Both can be problematic in complex,
    degraded

    or partially contaminated evidence. Footprints can appear incomplete and distorted
    which makes

    the analysis challenging. Comparing footprints to databases can take a long time,
    and can also

    result in a large amount of potential errors. There is a need for automated, objective
    and scalable

    analysis tools.

    Machine learning has already been used in the forensic sector to classify blood
    spatter, match

    shoeprints and identify victim demographics. However there are limitations. Most
    are single evi-

    dence types, not using machine learning across a variety of individually relevant
    evidence. Sample

    sizes t'
  - 'Enhancing Detection of Bloodstain Patterns and Footprint Impressions using Deep
    Learning

    4. Methodology

    This module uses a multi-task network to predict gender and age group (classiﬁcation).
    As well

    as predicting height (regression). The network uses categorical cross entropy
    loss to predict gender

    and age group. Mean square error loss is used to approximate the height of the
    person.

    4.5

    Interpretation and Reporting

    Rather than providing deterministic results, this provides probabilistic conﬁdence
    values. When

    analysing a bloodstain image the programme gives the user information on how conﬁdent
    it is that

    the stain is blood or non-blood. It also gives information on what mechanism is
    most likely and

    the top scenarios with supporting factors. This includes things such as how much
    of the sta'
- source_sentence: 'Represent this sentence for searching relevant passages: How does
    the footprint module''s performance on the UNB StepUP-P150 dataset reflect the
    model''s ability to distinguish between different footprint characteristics?'
  sentences:
  - ' ranked scenario hypotheses

    with supporting cues. The hypothesis scores are modest and sometimes close to
    one another (for

    instance 16.1% against 16.0% for the radial impact burst), so they are best read
    as a ranked aid to

    the practitioner’s reasoning rather than as a deﬁnitive verdict.

    5.3

    Footprint Classiﬁcation Results

    The footprint module was evaluated on the UNB StepUP-P150 dataset to evaluate
    the accuracy of

    demographic prediction. The quantitative results for gender classiﬁcation are
    shown in Table 5.2.

    The model derived from the ResNet-18 architecture achieved an accuracy of 91.6%.
    There were

    no signiﬁcant diﬀerences in the precision, recall and F1-score indicating appropriate
    features were

    learned in order to distinguish between the diﬀerent footprint shapes, sizes and
    pressure di'
  - 'Enhancing Detection of Bloodstain Patterns and Footprint Impressions using Deep
    Learning

    4. Methodology

    This module uses a multi-task network to predict gender and age group (classiﬁcation).
    As well

    as predicting height (regression). The network uses categorical cross entropy
    loss to predict gender

    and age group. Mean square error loss is used to approximate the height of the
    person.

    4.5

    Interpretation and Reporting

    Rather than providing deterministic results, this provides probabilistic conﬁdence
    values. When

    analysing a bloodstain image the programme gives the user information on how conﬁdent
    it is that

    the stain is blood or non-blood. It also gives information on what mechanism is
    most likely and

    the top scenarios with supporting factors. This includes things such as how much
    of the sta'
  - ' ranked scenario hypotheses

    with supporting cues. The hypothesis scores are modest and sometimes close to
    one another (for

    instance 16.1% against 16.0% for the radial impact burst), so they are best read
    as a ranked aid to

    the practitioner’s reasoning rather than as a deﬁnitive verdict.

    5.3

    Footprint Classiﬁcation Results

    The footprint module was evaluated on the UNB StepUP-P150 dataset to evaluate
    the accuracy of

    demographic prediction. The quantitative results for gender classiﬁcation are
    shown in Table 5.2.

    The model derived from the ResNet-18 architecture achieved an accuracy of 91.6%.
    There were

    no signiﬁcant diﬀerences in the precision, recall and F1-score indicating appropriate
    features were

    learned in order to distinguish between the diﬀerent footprint shapes, sizes and
    pressure di'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on BAAI/bge-base-en-v1.5

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [BAAI/bge-base-en-v1.5](https://huggingface.co/BAAI/bge-base-en-v1.5). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [BAAI/bge-base-en-v1.5](https://huggingface.co/BAAI/bge-base-en-v1.5) <!-- at revision a5beb1e3e68b9ab74eb54cfd186867f64f240e1a -->
- **Maximum Sequence Length:** 512 tokens
- **Output Dimensionality:** 768 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
  (1): Pooling({'embedding_dimension': 768, 'pooling_mode': 'cls', 'include_prompt': True})
  (2): Normalize({})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    "Represent this sentence for searching relevant passages: How does the footprint module's performance on the UNB StepUP-P150 dataset reflect the model's ability to distinguish between different footprint characteristics?",
    ' ranked scenario hypotheses\nwith supporting cues. The hypothesis scores are modest and sometimes close to one another (for\ninstance 16.1% against 16.0% for the radial impact burst), so they are best read as a ranked aid to\nthe practitioner’s reasoning rather than as a deﬁnitive verdict.\n5.3\nFootprint Classiﬁcation Results\nThe footprint module was evaluated on the UNB StepUP-P150 dataset to evaluate the accuracy of\ndemographic prediction. The quantitative results for gender classiﬁcation are shown in Table 5.2.\nThe model derived from the ResNet-18 architecture achieved an accuracy of 91.6%. There were\nno signiﬁcant diﬀerences in the precision, recall and F1-score indicating appropriate features were\nlearned in order to distinguish between the diﬀerent footprint shapes, sizes and pressure di',
    ' ranked scenario hypotheses\nwith supporting cues. The hypothesis scores are modest and sometimes close to one another (for\ninstance 16.1% against 16.0% for the radial impact burst), so they are best read as a ranked aid to\nthe practitioner’s reasoning rather than as a deﬁnitive verdict.\n5.3\nFootprint Classiﬁcation Results\nThe footprint module was evaluated on the UNB StepUP-P150 dataset to evaluate the accuracy of\ndemographic prediction. The quantitative results for gender classiﬁcation are shown in Table 5.2.\nThe model derived from the ResNet-18 architecture achieved an accuracy of 91.6%. There were\nno signiﬁcant diﬀerences in the precision, recall and F1-score indicating appropriate features were\nlearned in order to distinguish between the diﬀerent footprint shapes, sizes and pressure di',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.6192, 0.6192],
#         [0.6192, 1.0000, 1.0000],
#         [0.6192, 1.0000, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 113 training samples
* Columns: <code>anchor</code> and <code>positive</code>
* Approximate statistics based on the first 100 samples:
  |          | anchor                                                                             | positive                                                                             |
  |:---------|:-----------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
  | type     | string                                                                             | string                                                                               |
  | modality | text                                                                               | text                                                                                 |
  | details  | <ul><li>min: 21 tokens</li><li>mean: 27.56 tokens</li><li>max: 36 tokens</li></ul> | <ul><li>min: 59 tokens</li><li>mean: 153.87 tokens</li><li>max: 256 tokens</li></ul> |
* Samples:
  | anchor                                                                                                                                                                        | positive                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
  |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>Represent this sentence for searching relevant passages: What are the five classes included in the bloodstain dataset used for training the deep learning model?</code> | <code>Enhancing Detection of Bloodstain Patterns and Footprint Impressions using Deep Learning<br>3. Materials and Methods<br>Chapter 3<br>Materials and Methods<br>3.1<br>Datasets<br>Publicly available forensic datasets were used to train and validate the system, which supports<br>reproducibility and unbiased evaluation.<br>• Bloodstain dataset: Roughly 2,700 labeled bloodstain photographs retrieved from the<br>CSAFE, Noblis, Figshare, and Mendeley repositories. The dataset contains ﬁve equally rep-<br>resented classes: drip, impact, cast-oﬀ, transfer, and expirated. The ground truth labels come<br>from annotations in the datasets together with expert-generated metadata.<br>• Footprint dataset: 2,400 barefoot footprint images from the UNB StepUP-P150 dataset.<br>Each image carries ground-truth labels for the gender, height, and age g</code> |
  | <code>Represent this sentence for searching relevant passages: How many barefoot footprint images are included in the UNB StepUP-P150 dataset used for the study?</code>      | <code>Enhancing Detection of Bloodstain Patterns and Footprint Impressions using Deep Learning<br>3. Materials and Methods<br>Chapter 3<br>Materials and Methods<br>3.1<br>Datasets<br>Publicly available forensic datasets were used to train and validate the system, which supports<br>reproducibility and unbiased evaluation.<br>• Bloodstain dataset: Roughly 2,700 labeled bloodstain photographs retrieved from the<br>CSAFE, Noblis, Figshare, and Mendeley repositories. The dataset contains ﬁve equally rep-<br>resented classes: drip, impact, cast-oﬀ, transfer, and expirated. The ground truth labels come<br>from annotations in the datasets together with expert-generated metadata.<br>• Footprint dataset: 2,400 barefoot footprint images from the UNB StepUP-P150 dataset.<br>Each image carries ground-truth labels for the gender, height, and age g</code> |
  | <code>Represent this sentence for searching relevant passages: What types of ground-truth labels are provided for the footprint images in the UNB StepUP-P150 dataset?</code> | <code>Enhancing Detection of Bloodstain Patterns and Footprint Impressions using Deep Learning<br>3. Materials and Methods<br>Chapter 3<br>Materials and Methods<br>3.1<br>Datasets<br>Publicly available forensic datasets were used to train and validate the system, which supports<br>reproducibility and unbiased evaluation.<br>• Bloodstain dataset: Roughly 2,700 labeled bloodstain photographs retrieved from the<br>CSAFE, Noblis, Figshare, and Mendeley repositories. The dataset contains ﬁve equally rep-<br>resented classes: drip, impact, cast-oﬀ, transfer, and expirated. The ground truth labels come<br>from annotations in the datasets together with expert-generated metadata.<br>• Footprint dataset: 2,400 barefoot footprint images from the UNB StepUP-P150 dataset.<br>Each image carries ground-truth labels for the gender, height, and age g</code> |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Evaluation Dataset

#### Unnamed Dataset

* Size: 10 evaluation samples
* Columns: <code>anchor</code> and <code>positive</code>
* Approximate statistics based on the first 10 samples:
  |          | anchor                                                                            | positive                                                                             |
  |:---------|:----------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
  | type     | string                                                                            | string                                                                               |
  | modality | text                                                                              | text                                                                                 |
  | details  | <ul><li>min: 21 tokens</li><li>mean: 28.6 tokens</li><li>max: 43 tokens</li></ul> | <ul><li>min: 145 tokens</li><li>mean: 164.8 tokens</li><li>max: 174 tokens</li></ul> |
* Samples:
  | anchor                                                                                                                                                                                                                                   | positive                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
  |:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>Represent this sentence for searching relevant passages: What is the accuracy rate of the model based on the ResNet-18 architecture for gender classification in the footprint module?</code>                                      | <code> ranked scenario hypotheses<br>with supporting cues. The hypothesis scores are modest and sometimes close to one another (for<br>instance 16.1% against 16.0% for the radial impact burst), so they are best read as a ranked aid to<br>the practitioner’s reasoning rather than as a deﬁnitive verdict.<br>5.3<br>Footprint Classiﬁcation Results<br>The footprint module was evaluated on the UNB StepUP-P150 dataset to evaluate the accuracy of<br>demographic prediction. The quantitative results for gender classiﬁcation are shown in Table 5.2.<br>The model derived from the ResNet-18 architecture achieved an accuracy of 91.6%. There were<br>no signiﬁcant diﬀerences in the precision, recall and F1-score indicating appropriate features were<br>learned in order to distinguish between the diﬀerent footprint shapes, sizes and pressure di</code> |
  | <code>Represent this sentence for searching relevant passages: Why are the hypothesis scores described as modest and close to one another in the ranked scenario hypotheses?</code>                                                      | <code> ranked scenario hypotheses<br>with supporting cues. The hypothesis scores are modest and sometimes close to one another (for<br>instance 16.1% against 16.0% for the radial impact burst), so they are best read as a ranked aid to<br>the practitioner’s reasoning rather than as a deﬁnitive verdict.<br>5.3<br>Footprint Classiﬁcation Results<br>The footprint module was evaluated on the UNB StepUP-P150 dataset to evaluate the accuracy of<br>demographic prediction. The quantitative results for gender classiﬁcation are shown in Table 5.2.<br>The model derived from the ResNet-18 architecture achieved an accuracy of 91.6%. There were<br>no signiﬁcant diﬀerences in the precision, recall and F1-score indicating appropriate features were<br>learned in order to distinguish between the diﬀerent footprint shapes, sizes and pressure di</code> |
  | <code>Represent this sentence for searching relevant passages: How does the footprint module's performance on the UNB StepUP-P150 dataset reflect the model's ability to distinguish between different footprint characteristics?</code> | <code> ranked scenario hypotheses<br>with supporting cues. The hypothesis scores are modest and sometimes close to one another (for<br>instance 16.1% against 16.0% for the radial impact burst), so they are best read as a ranked aid to<br>the practitioner’s reasoning rather than as a deﬁnitive verdict.<br>5.3<br>Footprint Classiﬁcation Results<br>The footprint module was evaluated on the UNB StepUP-P150 dataset to evaluate the accuracy of<br>demographic prediction. The quantitative results for gender classiﬁcation are shown in Table 5.2.<br>The model derived from the ResNet-18 architecture achieved an accuracy of 91.6%. There were<br>no signiﬁcant diﬀerences in the precision, recall and F1-score indicating appropriate features were<br>learned in order to distinguish between the diﬀerent footprint shapes, sizes and pressure di</code> |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `learning_rate`: 2e-05
- `warmup_steps`: 0.1
- `fp16`: True
- `per_device_eval_batch_size`: 16
- `batch_sampler`: no_duplicates

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 2e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0.1
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1.0
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: True
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 16
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: None
- `fsdp_config`: None
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `warmup_ratio`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: no_duplicates
- `multi_dataset_batch_sampler`: proportional
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch | Step | Training Loss | Validation Loss |
|:-----:|:----:|:-------------:|:---------------:|
| 0.625 | 5    | 1.4530        | -               |
| 1.0   | 8    | -             | 0.1881          |
| 1.25  | 10   | 1.0064        | -               |
| 1.875 | 15   | 0.7489        | -               |
| 2.0   | 16   | -             | 0.1457          |
| 2.5   | 20   | 0.5233        | -               |
| 3.0   | 24   | -             | 0.1369          |


### Training Time
- **Training**: 12.4 seconds
- **Evaluation**: 0.4 seconds
- **Total**: 12.8 seconds

### Framework Versions
- Python: 3.14.5
- Sentence Transformers: 5.6.0
- Transformers: 5.13.1
- PyTorch: 2.11.0+cu128
- Accelerate: 1.15.0
- Datasets: 5.1.0
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->