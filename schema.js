const Joi = require('joi');

module.exports = {
    'Predict': Joi.object().keys({
        sentiment: Joi.number().required(),
        postLength: Joi.number().required(),
        hashTagCount: Joi.number().required(),
        contentURLCount: Joi.number().required(),
        likeCount: Joi.number().required(),
        shareCount: Joi.number().required(),
        commentCount: Joi.number().required(),
        followersCount: Joi.number().required(),
        followingCount: Joi.number().required(),
        tweetCount: Joi.number().required(),
        gender: Joi.number().required(),
        secondsElapsed: Joi.number().required()
    })
}