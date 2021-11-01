"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 850
SCREEN_TITLE = "Break the Targets!"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 27
GRAVITY = 2
PLAYER_JUMP_SPEED = 47


TARGET_SCALING = TILE_SCALING
BACKGROUND_MUSIC = 1

LAYER_NAME_TARGETS = "Targets"
LAYER_NAME_BULLETS = "Bullets"

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        # super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        super().__init__()


        # self.music_game = []
        # self.playing_song = 0
        # self.song = None
        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        self.shoot_pressed = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.target_count = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("soundEffects/targetBreakSound.wav")
        self.jump_sound = arcade.load_sound("soundEffects/jumpSound.wav")
        self.target_break_sound = arcade.load_sound("soundEffects/targetBreakSound.wav")
        self.shoot_sound = arcade.load_sound("soundEffects/blast.wav")
        self.audio_name = arcade.sound.load_sound("music/breakTheTargets.mp3")
        # self.click_sound = arcade.sound.load_sound("soundEffects/clickSound.wav")
        # BACKGROUND_MUSIC = []

        arcade.set_background_color(arcade.csscolor.SALMON)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        arcade.sound.play_sound(self.audio_name)

        # BACKGROUND_MUSIC = ["music/breakTheTargets.mp3"]
        # arcade.play_sound(BACKGROUND_MUSIC)
        
        # Setup the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = "pleaseWORKTest.json"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,

            "Targets": {
                "use_spatial_hash": True,
            }
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.target_count = 0


        self.target_break = 0

        # Create the Player Sprite lists
        player_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = "images/charLeft.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list(LAYER_NAME_BULLETS)

        # --- Other stuff
        # Set the background color
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.scene.get_sprite_list("Platforms"), GRAVITY
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        target_text = f"Targets: {self.target_count}"
        arcade.draw_text(
            target_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # if key == arcade.key.P:
        #     self.shoot_pressed = True
        #     arcade.play_sound(self.click_sound)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

        # if key == arcade.key.P:
        #     self.shoot_pressed = False

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        target_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list(LAYER_NAME_TARGETS)
        )
        # print(target_hit_list)

        for target in target_hit_list:
            target.remove_from_sprite_lists()
            self.target_count + 1
            arcade.play_sound(self.target_break_sound)


            
    
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_TARGETS,

            ],
        )

        if self.target_count == 11:
            view = GameOverView()
            self.window.view(view)

        # Position the camera
        self.center_camera_to_player()




def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


    


if __name__ == "__main__":
    main()