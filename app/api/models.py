from django.db import models


class TGMessageManager(models.Manager):
    def create_message(self, **kwargs):
        self.message_id = kwargs.get('message_id')
        self.sender_id = kwargs.get('sender_id')
        self.message_date = kwargs.get('message_date')
        self.channel_name = kwargs.get('channel_name')
        self.channel_id = kwargs.get('channel_id')
        self.status = kwargs.get('status')
        self.raw_text = kwargs.get('raw_text')
        self.raw_text = ' '.join([line.strip() for line in self.raw_text.strip().splitlines() if line.strip()])
        message = self.create(message_id=self.message_id, sender_id=self.sender_id, message_date=self.message_date, channel_name=self.channel_name, channel_id=self.channel_id, status=self.status, raw_text=self.raw_text)

        return message


class TGMessage(models.Model):
    id = models.AutoField(primary_key=True)
    message_id = models.CharField(max_length=255)
    sender_id = models.CharField(max_length=255)
    received_date = models.DateTimeField(auto_now_add=True)
    message_date = models.DateTimeField(auto_now_add=True)
    channel_name = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    raw_text = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    ack = models.BooleanField(default=False)

    objects = TGMessageManager()



class TradeTest(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    forex_account_number = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    forex_pair = models.CharField(max_length=255)
    entry = models.FloatField()
    action = models.CharField(max_length=255)
    lotsize = models.FloatField()
    stop_loss1 = models.FloatField()
    stop_loss2 = models.FloatField()
    stop_loss3 = models.FloatField()
    stop_loss4 = models.FloatField()
    stop_loss5 = models.FloatField()
    stop_loss_pips_planned = models.FloatField()
    stop_loss_pips_actual = models.FloatField()
    stop_loss_count = models.IntegerField()

    take_profit1 = models.FloatField()
    take_profit1_adj = models.FloatField()
    take_profit1_pips_planned = models.FloatField()
    take_profit1_pips_actual = models.FloatField()

    take_profit2 = models.FloatField()
    take_profit2_adj = models.FloatField()
    take_profit2_pips_planned = models.FloatField()
    take_profit2_pips_actual = models.FloatField()

    take_profit3 = models.FloatField()
    take_profit3_adj = models.FloatField()
    take_profit3_pips_planned = models.FloatField()
    take_profit3_pips_actual = models.FloatField()

    take_profit4 = models.FloatField()
    take_profit4_adj = models.FloatField()
    take_profit4_pips_planned = models.FloatField()
    take_profit4_pips_actual = models.FloatField()

    take_profit5 = models.FloatField()
    take_profit5_adj = models.FloatField()
    take_profit5_pips_planned = models.FloatField()
    take_profit5_pips_actual = models.FloatField()

    take_profit_count = models.IntegerField()
    take_profit_total_actual = models.FloatField()

    total_trades = models.IntegerField()
    origin = models.CharField(max_length=255)
    strategy = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    tg_message_id = models.CharField(max_length=255)
    tg_sender_id = models.CharField(max_length=255)
    tg_date = models.DateTimeField(auto_now_add=True)
    mt4_ticket_id = models.CharField(max_length=255)
    mt4_magic_number = models.CharField(max_length=255)
    mt4_open_time = models.DateTimeField(auto_now_add=True)


