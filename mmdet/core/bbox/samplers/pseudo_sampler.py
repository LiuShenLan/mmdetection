import torch

from ..builder import BBOX_SAMPLERS
from .base_sampler import BaseSampler
from .sampling_result import SamplingResult


@BBOX_SAMPLERS.register_module()
class PseudoSampler(BaseSampler):
    """A pseudo sampler that does not do sampling actually."""

    def __init__(self, **kwargs):
        pass

    def _sample_pos(self, **kwargs):
        """Sample positive samples."""
        raise NotImplementedError

    def _sample_neg(self, **kwargs):
        """Sample negative samples."""
        raise NotImplementedError

    def sample(self, assign_result, bboxes, gt_bboxes, gt_keypoints, **kwargs):
        """Directly returns the positive and negative indices  of samples.

        Args:
            assign_result (:obj:`AssignResult`): Assigned results
            bboxes (torch.Tensor): Bounding boxes           [all_h*w,4]
            gt_bboxes (torch.Tensor): Ground truth boxes    [k,4]

        Returns:
            :obj:`SamplingResult`: sampler results
        """
        pos_inds = torch.nonzero(   # [k] 每个元素为bbox的index
            assign_result.gt_inds > 0, as_tuple=False).squeeze(-1).unique()
        # assign_result.gt_inds:[allh*w],背景为0,bbox中心点为bbox_index(既从1到k)
        neg_inds = torch.nonzero(   # [all_h*w-k] 每个元素为range(all_h*w),去掉bbox的index
            assign_result.gt_inds == 0, as_tuple=False).squeeze(-1).unique()
        gt_flags = bboxes.new_zeros(bboxes.shape[0], dtype=torch.uint8)     # [all_h*w] 全零
        sampling_result = SamplingResult(pos_inds, neg_inds, bboxes, gt_bboxes, gt_keypoints,
                                         assign_result, gt_flags)
        return sampling_result
