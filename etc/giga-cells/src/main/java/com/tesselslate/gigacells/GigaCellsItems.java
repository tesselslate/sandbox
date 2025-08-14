package com.tesselslate.gigacells;

import net.minecraft.world.item.Item;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.ArrayList;

import appeng.api.stacks.AEKeyType;
import com.mojang.datafixers.util.Pair;

public final class GigaCellsItems {
    private static final DeferredRegister<Item> REGISTER =
            DeferredRegister.create(ForgeRegistries.ITEMS, GigaCells.MODID);
    private static ArrayList<Pair<String, Item>> ITEMS = new ArrayList<>();

    public static final Item ITEM_CELL_HOUSING_MK1 = item("item_cell_housing_mk1", new Item(new Item.Properties()));
    public static final Item ITEM_CELL_HOUSING_MK2 = item("item_cell_housing_mk2", new Item(new Item.Properties()));

    public static final Item FLUID_CELL_HOUSING_MK1 = item("fluid_cell_housing_mk1", new Item(new Item.Properties()));
    public static final Item FLUID_CELL_HOUSING_MK2 = item("fluid_cell_housing_mk2", new Item(new Item.Properties()));

    public static final Item[] GIGABYTE_CELL_COMPONENTS;
    public static final Item[] TERABYTE_CELL_COMPONENTS;

    public static final LargeStorageCell[] GIGABYTE_ITEM_CELLS;
    public static final LargeStorageCell[] TERABYTE_ITEM_CELLS;

    public static final LargeStorageCell[] GIGABYTE_FLUID_CELLS;
    public static final LargeStorageCell[] TERABYTE_FLUID_CELLS;

    static {
        GIGABYTE_CELL_COMPONENTS = new Item[5];
        TERABYTE_CELL_COMPONENTS = new Item[5];

        GIGABYTE_ITEM_CELLS = new LargeStorageCell[5];
        TERABYTE_ITEM_CELLS = new LargeStorageCell[5];

        GIGABYTE_FLUID_CELLS = new LargeStorageCell[5];
        TERABYTE_FLUID_CELLS = new LargeStorageCell[5];

        long kilobytes = 1048576;
        long bytesPerType = 8388608;
        double drain = 16.0f;

        // Gigabyte cells
        for (int i = 0; i < 5; i++) {
            int size = 1 << (i * 2);

            GIGABYTE_CELL_COMPONENTS[i] =
                    item(String.format("cell_component_%dg", size), new Item(new Item.Properties()));

            GIGABYTE_ITEM_CELLS[i] = item(
                    String.format("item_cell_%dg", size),
                    new LargeStorageCell(
                            new Item.Properties().stacksTo(1),
                            GIGABYTE_CELL_COMPONENTS[i],
                            ITEM_CELL_HOUSING_MK1,
                            drain,
                            kilobytes,
                            bytesPerType,
                            63,
                            AEKeyType.items()));

            GIGABYTE_FLUID_CELLS[i] = item(
                    String.format("fluid_cell_%dg", size),
                    new LargeStorageCell(
                            new Item.Properties().stacksTo(1),
                            GIGABYTE_CELL_COMPONENTS[i],
                            FLUID_CELL_HOUSING_MK1,
                            drain,
                            kilobytes,
                            bytesPerType,
                            18,
                            AEKeyType.fluids()));

            kilobytes *= 4;
            bytesPerType *= 4;
            drain *= 4;
        }

        // Terabyte cells
        for (int i = 0; i < 5; i++) {
            int size = 1 << (i * 2);

            TERABYTE_CELL_COMPONENTS[i] =
                    item(String.format("cell_component_%dt", size), new Item(new Item.Properties()));

            TERABYTE_ITEM_CELLS[i] = item(
                    String.format("item_cell_%dt", size),
                    new LargeStorageCell(
                            new Item.Properties().stacksTo(1),
                            TERABYTE_CELL_COMPONENTS[i],
                            ITEM_CELL_HOUSING_MK2,
                            drain,
                            kilobytes,
                            bytesPerType,
                            63,
                            AEKeyType.items()));

            TERABYTE_FLUID_CELLS[i] = item(
                    String.format("fluid_cell_%dt", size),
                    new LargeStorageCell(
                            new Item.Properties().stacksTo(1),
                            TERABYTE_CELL_COMPONENTS[i],
                            FLUID_CELL_HOUSING_MK2,
                            drain,
                            kilobytes,
                            bytesPerType,
                            18,
                            AEKeyType.fluids()));

            kilobytes *= 4;
            bytesPerType *= 4;
            drain *= 4;
        }
    }

    static void init(IEventBus eventBus) {
        REGISTER.register(eventBus);

        for (var pair : ITEMS) {
            REGISTER.register(pair.getFirst(), () -> pair.getSecond());
        }

        GigaCells.LOGGER.debug("Registered GigaCells items");
    }

    private static <T extends Item> T item(String id, T item) {
        ITEMS.add(new Pair<>(id, item));

        return item;
    }
}
