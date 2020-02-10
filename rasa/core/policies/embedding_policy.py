import logging
from typing import Any, Dict, Optional, Text

from rasa.core.constants import DEFAULT_POLICY_PRIORITY
from rasa.core.featurizers import TrackerFeaturizer
from rasa.core.policies.ted_policy import TEDPolicy
from rasa.constants import DOCS_BASE_URL
from rasa.utils.tensorflow.constants import (
    HIDDEN_LAYERS_SIZES_LABEL,
    NUM_TRANSFORMER_LAYERS,
    BATCH_SIZES,
    BATCH_STRATEGY,
    EPOCHS,
    RANDOM_SEED,
    RANKING_LENGTH,
    LOSS_TYPE,
    SIMILARITY_TYPE,
    NUM_NEG,
    EVAL_NUM_EXAMPLES,
    EVAL_NUM_EPOCHS,
    C_EMB,
    C2,
    SCALE_LOSS,
    USE_MAX_SIM_NEG,
    MU_NEG,
    MU_POS,
    EMBED_DIM,
    HIDDEN_LAYERS_SIZES_DIALOGUE,
    TRANSFORMER_SIZE,
    MAX_SEQ_LENGTH,
    NUM_HEADS,
    DROPRATE_DIALOGUE,
    DROPRATE_LABEL,
)
from rasa.utils.common import raise_warning
from rasa.utils.tensorflow.tf_models import RasaModel

logger = logging.getLogger(__name__)


class EmbeddingPolicy(TEDPolicy):
    """Transformer Embedding Dialogue Policy (TEDP)

    The policy used in our paper https://arxiv.org/abs/1910.00486
    """

    # default properties (DOC MARKER - don't remove)
    defaults = {
        # nn architecture
        # a list of hidden layers sizes before user embed layer
        # number of hidden layers is equal to the length of this list
        HIDDEN_LAYERS_SIZES_DIALOGUE: [],
        # a list of hidden layers sizes before bot embed layer
        # number of hidden layers is equal to the length of this list
        HIDDEN_LAYERS_SIZES_LABEL: [],
        # number of units in transformer
        TRANSFORMER_SIZE: 128,
        # number of transformer layers
        NUM_TRANSFORMER_LAYERS: 1,
        # max sequence length if pos_encoding='emb'
        MAX_SEQ_LENGTH: 256,
        # number of attention heads in transformer
        NUM_HEADS: 4,
        # training parameters
        # initial and final batch sizes:
        # batch size will be linearly increased for each epoch
        BATCH_SIZES: [8, 32],
        # how to create batches
        BATCH_STRATEGY: "balanced",  # string 'sequence' or 'balanced'
        # number of epochs
        EPOCHS: 1,
        # set random seed to any int to get reproducible results
        RANDOM_SEED: None,
        # embedding parameters
        # dimension size of embedding vectors
        EMBED_DIM: 20,
        # the type of the similarity
        NUM_NEG: 20,
        # flag if minimize only maximum similarity over incorrect labels
        SIMILARITY_TYPE: "auto",  # string 'auto' or 'cosine' or 'inner'
        # the type of the loss function
        LOSS_TYPE: "softmax",  # string 'softmax' or 'margin'
        # number of top actions to normalize scores for softmax loss_type
        # set to 0 to turn off normalization
        RANKING_LENGTH: 10,
        # how similar the algorithm should try
        # to make embedding vectors for correct labels
        MU_POS: 0.8,  # should be 0.0 < ... < 1.0 for 'cosine'
        # maximum negative similarity for incorrect labels
        MU_NEG: -0.2,  # should be -1.0 < ... < 1.0 for 'cosine'
        # the number of incorrect labels, the algorithm will minimize
        # their similarity to the user input during training
        USE_MAX_SIM_NEG: True,  # flag which loss function to use
        # scale loss inverse proportionally to confidence of correct prediction
        SCALE_LOSS: True,
        # regularization
        # the scale of L2 regularization
        C2: 0.001,
        # the scale of how important is to minimize the maximum similarity
        # between embeddings of different labels
        C_EMB: 0.8,
        # dropout rate for dial nn
        DROPRATE_DIALOGUE: 0.1,
        # dropout rate for bot nn
        DROPRATE_LABEL: 0.0,
        # visualization of accuracy
        # how often calculate validation accuracy
        EVAL_NUM_EPOCHS: 20,  # small values may hurt performance
        # how many examples to use for hold out validation set
        EVAL_NUM_EXAMPLES: 0,  # large values may hurt performance
    }
    # end default properties (DOC MARKER - don't remove)

    def __init__(
        self,
        featurizer: Optional[TrackerFeaturizer] = None,
        priority: int = DEFAULT_POLICY_PRIORITY,
        max_history: Optional[int] = None,
        model: Optional[RasaModel] = None,
        **kwargs: Dict[Text, Any],
    ) -> None:

        super().__init__(featurizer, priority, max_history, model, **kwargs)

        raise_warning(
            f"'EmbeddingPolicy' is deprecated. Use 'TEDPolicy' instead.",
            category=DeprecationWarning,
            docs=f"{DOCS_BASE_URL}/core/policies/",
        )
