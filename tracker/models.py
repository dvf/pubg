from json import JSONDecodeError

from django.db import models

from tracker import clients
import logging

logger = logging.getLogger(__name__)


class PlayerManager(models.Manager):
    def fetch(self, name: str):
        responses = clients.player_information(name)
        for response in responses:
            if response.status_code != 200:
                logger.error('Bad Response', extra={'name': name, 'status_code': response.status_code})
                continue

            try:
                r = response.json()
            except JSONDecodeError:
                logger.error('Could not decode JSON', extra={'name': name, 'status_code': response.status_code})
                continue

            # Make sure the shard exists
            response_shard = r['data'][0]['attributes']['shardId']
            shard, created = Shard.objects.get_or_create(name=response_shard)

            player, created = self.get_or_create(
                name=r['data'][0]['attributes']['name'],
                remote_id=r['data'][0]['id'],
            )

            player.shards.add(shard)

            matches = []
            for match in r['data'][0]['relationships']['matches']['data']:
                matches.append(Match.objects.get_or_create(remote_id=match['id'])[0])

            player.matches.add(*matches)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Shard(BaseModel):
    name = models.CharField(max_length=20)


class Player(BaseModel):
    objects = PlayerManager()

    remote_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    shards = models.ManyToManyField('Shard')
    matches = models.ManyToManyField('Match')

    class Meta:
        indexes = [
            models.Index(fields=['name', 'remote_id']),
        ]


class Match(BaseModel):
    remote_id = models.UUIDField()
