def eager_load(get_queryset):
    """
    Use as a decorator around the get_queryset method to prefetch/ select related
    data provided by the serializer layer

    :param get_queryset: overriding DRF get_queryset method
    :return: Data prefetched/select_related at serializer level
    """

    def eager_loading_queryset(self, *args, **kwargs):
        # vanilla get_queryset
        queryset = get_queryset(self, *args, **kwargs)

        # Eager load specified fields
        if (
            getattr(self.get_serializer_class(), "setup_eager_loading", None)
            is not None
        ):
            queryset = self.get_serializer_class().setup_eager_loading(queryset)

        return queryset

    return eager_loading_queryset
