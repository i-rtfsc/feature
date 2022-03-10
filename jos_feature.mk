ifneq ($(TARGET_PRODUCT),)

LOCAL_JOS_FEATURE_OUT := ${TOP}/vendor/journeyOS/feature/build_out
LOCAL_JOS_FEATURE_ROOT := ${TOP}/vendor/journeyOS/feature

LOCAL_JOS_FEATURE_CMD := python $(TOP)/vendor/journeyOS/feature/tools/feature.py \
                --product $(TARGET_PRODUCT) \
                --root $(LOCAL_JOS_FEATURE_ROOT) \
                --out $(LOCAL_JOS_FEATURE_OUT)

_result_:=$(shell $(LOCAL_JOS_FEATURE_CMD))

include $(LOCAL_JOS_FEATURE_ROOT)/common_feature.mk

include $(LOCAL_JOS_FEATURE_OUT)/makefile/JosFeature.mk

endif #TARGET_PRODUCT
