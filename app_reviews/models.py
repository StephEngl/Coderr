from django.db import models


class Review(models.Model):
    """
    Model representing a review/rating given by a customer to a business user.

    Behavior:
        - Each review links one customer (reviewer) to one business user (business_user).
        - Reviews are deleted if the associated business user or reviewer is deleted.
        - Rating is restricted to the range 1-5.
        - Description is optional and can be left blank.
    """

    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    business_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('auth.User', related_name='written_reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    description = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')