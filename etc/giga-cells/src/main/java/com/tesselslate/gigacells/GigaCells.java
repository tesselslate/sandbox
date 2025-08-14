package com.tesselslate.gigacells;

import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

import org.slf4j.Logger;

import appeng.api.storage.StorageCells;
import com.mojang.logging.LogUtils;

@Mod(GigaCells.MODID)
public class GigaCells {
    public static final String MODID = "gigacells";
    static final Logger LOGGER = LogUtils.getLogger();

    public GigaCells() {
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();

        GigaCellsItems.init(modEventBus);

        StorageCells.addCellHandler(LargeCellHandler.INSTANCE);
    }
}
